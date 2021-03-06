from django.contrib.auth.models import User

from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from fpdc.releases.models import Release

DATA = {
    "release_id": "fedora-27",
    "short": "fedora",
    "name": "Fedora",
    "version": 27,
    "release_date": "2017-11-14",
    "eol_date": "2018-11-30",
    "sigkey": "0xdeadbeef",
}


class ReleaseViewTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = mixer.blend(User)

    def test_create_release(self):
        url = reverse("v1:release-list")
        self.client.force_authenticate(self.__class__.user)
        response = self.client.post(url, DATA, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Release.objects.count() == 1
        assert Release.objects.get().release_id == "fedora-27"

    def test_update_release(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        self.client.force_authenticate(self.__class__.user)
        response = self.client.put(url, DATA, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Release.objects.count() == 1
        assert Release.objects.get().release_id == "fedora-27"

    def test_partial_update_release(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        data = {"release_id": "fedora-28"}
        self.client.force_authenticate(self.__class__.user)
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Release.objects.count() == 1
        assert Release.objects.get().release_id == "fedora-28"

    def test_delete_release(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        assert Release.objects.count() == 1
        self.client.force_authenticate(self.__class__.user)
        response = self.client.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Release.objects.count() == 0

    def test_get_release(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["release_id"] == release.release_id

    def test_get_release_list(self):
        mixer.cycle(5).blend(Release)
        url = reverse("v1:release-list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert Release.objects.count() == 5

    def test_create_release_unauthenticated(self):
        url = reverse("v1:release-list")
        response = self.client.post(url, DATA, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_release_unauthenticated(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        response = self.client.put(url, DATA, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_partial_update_release_unauthenticated(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        data = {"release_id": "fedora-28"}
        response = self.client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_release_unauthenticated(self):
        release = mixer.blend(Release)
        url = reverse("v1:release-detail", kwargs={"pk": release.pk})
        assert Release.objects.count() == 1
        response = self.client.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
