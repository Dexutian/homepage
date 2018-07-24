from django.conf import settings
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class HomepageTestCase(StaticLiveServerTestCase):
    def setUp(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
        )
        self.selenium = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=os.path.join(settings.MEDIA_ROOT, 'phantomjs.exe'))
        super(HomepageTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(HomepageTestCase, self).tearDown()

    def test_can_visit_homepage(self):
        self.selenium.get(
            '%s%s' % (self.live_server_url, "/")
        )
        self.assertIn("Django应用", self.selenium.title)