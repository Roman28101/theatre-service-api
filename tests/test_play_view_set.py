from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Play, Genre, Actor
from theatre.serializers import PlayListSerializer, PlayDetailSerializer

PLAY_URL = reverse("theatre:play-list")


def some_play(**params):
    defaults = {
        "title": "Nutcracker",
        "description": "Gold classic",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def detail_url(play_id: int):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@test.com",
            "user1234",
        )
        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        some_play()
        play_with_actors = some_play()
        play_with_actors_genres = some_play()

        genre1 = Genre.objects.create(name="music")
        genre2 = Genre.objects.create(name="comedy")

        actor1 = Actor.objects.create(first_name="Jamie", last_name="Foxx")
        actor2 = Actor.objects.create(first_name="Hugh", last_name="Jackman")

        play_with_actors.actors.add(actor1, actor2)
        play_with_actors_genres.actors.add(actor1, actor2)
        play_with_actors_genres.genres.add(genre1, genre2)
        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_play_filter(self):
        play_empty = some_play()
        play1 = some_play()
        play2 = some_play()

        genre = Genre.objects.create(name="drama")

        actor = Actor.objects.create(
            first_name="Christoph",
            last_name="Waltz"
        )

        play1.actors.add(actor)
        play2.actors.add(actor)
        play2.genres.add(genre)

        res_actors = self.client.get(
            PLAY_URL,
            {"actors": f"{actor.id}, {actor.id}"}
        )
        res_actors_genres = self.client.get(
            PLAY_URL,
            {"actors": f"{actor.id}"},
            {"genres": f"{genre.id}"}
        )

        serializer1 = PlayListSerializer(play_empty)
        serializer2 = PlayListSerializer(play1)
        serializer3 = PlayListSerializer(play2)

        self.assertIn(serializer2.data, res_actors.data)
        self.assertIn(serializer3.data, res_actors_genres.data)
        self.assertNotIn(serializer1.data, res_actors.data)
        self.assertNotIn(serializer1.data, res_actors_genres.data)

    def test_retrieve_play_detail(self):
        play = some_play()
        play.actors.add(Actor.objects.create(
            first_name="Jamie",
            last_name="Foxx")
        )
        play.genres.add(Genre.objects.create(name="action"))

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def create_play_forbidden(self):
        payload = {
            "title": "The Greatest Showman",
            "description": "Many good songs",
        }

        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@test.com",
            "admin1234",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):

        payload = {
            "title": "Play",
            "description": "Info about play",
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_actors_genres(self):
        genre = Genre.objects.create(name="comedy")
        actor = Actor.objects.create(
            first_name="Hugh",
            last_name="Jackman"
        )

        payload = {
            "title": "Play",
            "description": "Info about play",
            "genres": genre.id,
            "actors": actor.id
        }

        res = self.client.post(PLAY_URL, payload)
        movie = Play.objects.get(id=res.data["id"])
        genres = movie.genres.all()
        actors = movie.actors.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(genres.count(), 1)
        self.assertIn(genre, genres)
        self.assertEqual(actors.count(), 1)
        self.assertIn(actor, actors)

    def test_delete_not_allowed(self):
        play = some_play()
        url = detail_url(play.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
