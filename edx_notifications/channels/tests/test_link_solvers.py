"""
Unit tests for the resolvers.py file
"""

from django.test import TestCase

from edx_notifications.channels.link_resolvers import (
    BaseLinkResolver,
    MsgTypeToUrlLinkResolver,
)


class BadLinkResolver(BaseLinkResolver):
    """
    A test link resolver which should throw exceptions because
    it does not do what it is supposed to do per
    the abstract interface contract
    """

    def resolve(self, msg_type_name, link_name, params):
        """
        Simply call into our parent which show throw exception
        """
        return super(BadLinkResolver, self).resolve(msg_type_name, link_name, params)


class BaseLinkResolverTests(TestCase):
    """
    Assert that the abstract interface is right
    """

    def test_create_abstract_class(self):
        """
        Asserts that we cannot create an instance of the
        abstract class
        """
        with self.assertRaises(TypeError):
            BaseLinkResolver()  # pylint: disable=abstract-class-instantiated

    def test_throws_exception(self):
        """
        Confirms that the base abstract class will raise an exception
        """

        with self.assertRaises(NotImplementedError):
            BadLinkResolver().resolve(None, None, None)


class MsgTypeToUrlLinkResolverTests(TestCase):
    """
    Make sure things resolve as we expect them to
    """

    def test_resolve(self):
        """
        Assert we can resolve a well formed type_name, link_name, and params
        """

        resolver = MsgTypeToUrlLinkResolver({
            '_click_url': {
                # this will conver msg type 'test-type.type-with-links'
                # to /path/to/{param1}/url/{param2} with param subsitutations
                # that are passed in with the message
                'test-type.type-with-links': '/path/to/{param1}/url/{param2}'
            }
        })

        url = resolver.resolve(
            'test-type.type-with-links',
            '_click_url',
            {
                'param1': 'foo',
                'param2': 'bar',
            }
        )
        self.assertEqual(url, '/path/to/foo/url/bar')

    def test_missing_type(self):
        """
        Failure case when the msg_type cannot be found
        """

        resolver = MsgTypeToUrlLinkResolver({
            '_click_url': {
                # this will conver msg type 'test-type.type-with-links'
                # to /path/to/{param1}/url/{param2} with param subsitutations
                # that are passed in with the message
                'test-type.type-with-links': '/path/to/{param1}/url/{param2}'
            }
        })

        url = resolver.resolve(
            'test-type.missing-type',
            '_click_url',
            {
                'param1': 'foo',
                'param2': 'bar',
            }
        )
        self.assertIsNone(url)

    def test_missing_link_name(self):
        """
        Failure case when the link_name cannot be found
        """

        resolver = MsgTypeToUrlLinkResolver({
            '_click_url': {
                # this will conver msg type 'test-type.type-with-links'
                # to /path/to/{param1}/url/{param2} with param subsitutations
                # that are passed in with the message
                'test-type.type-with-links': '/path/to/{param1}/url/{param2}'
            }
        })

        url = resolver.resolve(
            'test-type.type-with-links',
            'missing_link_name',
            {
                'param1': 'foo',
                'param2': 'bar',
            }
        )
        self.assertIsNone(url)

    def test_missing_formatting_param(self):
        """
        Failure case wheen the msg_type cannot be found
        """

        resolver = MsgTypeToUrlLinkResolver({
            '_click_url': {
                # this will conver msg type 'test-type.type-with-links'
                # to /path/to/{param1}/url/{param2} with param subsitutations
                # that are passed in with the message
                'test-type.type-with-links': '/path/to/{param1}/url/{param2}'
            }
        })

        url = resolver.resolve(
            'test-type.type-with-links',
            '_click_url',
            {
                'param1': 'foo',
            }
        )
        self.assertIsNone(url)