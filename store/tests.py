from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking

# Index page
class IndexPageTestCase(TestCase):
  # test that index page returns a 200
  def test_index_page(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)

# Detail Page
class DetailPageTestCase(TestCase):
  # test that detail page returns a 200 if the item exists
  def test_detail_page_returns_200(self):
    album = Album.objects.create(title="test exists")
    response = self.client.get(reverse('store:detail', args=(album.id, )))
    self.assertEqual(response.status_code, 200)

  # test that detail page returns a 404 if the item does not exist
  def test_detail_page_returns_404(self):
    album = Album.objects.create(title="test exists")
    response = self.client.get(reverse('store:detail', args=(album.id + 1, )))
    self.assertEqual(response.status_code, 404)

# Booking Page
class BookinglPageTestCase(TestCase):
  def setUp(self):
    self.album = Album.objects.create(title="bookingAlbum")
    self.contact = Contact.objects.create(name="nom", email="nom@provider.com")

  # test that a new booking is made
  def test_booking_exists(self):
    self.setUp()
    oldBooking = Booking.objects.count()
    self.client.post(reverse('store:detail', args=(self.album.id,)), {'name':self.contact.name, 'email':self.contact.email})
    newBooking = Booking.objects.count()
    self.assertEqual(oldBooking + 1, newBooking)

  # test that a booking belongs to a contact
  def test_booking_contact(self):
    self.setUp()
    self.client.post(reverse('store:detail', args=(self.album.id,)), {'name':self.contact.name, 'email':self.contact.email})
    booking = Booking.objects.last()
    self.assertEqual(booking.contact.email, self.contact.email)

  # test that a booking belongs to an album
    # test that an album is not available after a booking is made