import unittest
from bs4 import BeautifulSoup
import unittest
from unittest.mock import patch
from unittest.mock import call
from job_alert import filter_jobs


class TestFilterJobs(unittest.TestCase):
    @patch('os.system')
    def test_filter_jobs(self, mock_system):
        html_doc = """
        <ul class="jobs-search__results-list">
          <li>
            <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card" data-entity-urn="urn:li:jobPosting:3326240771" data-search-id="CDfF3BXhv52/JAXxfr1HkA==" data-tracking-id="GQONh6GjtZPZWLigkqGGdw==" data-column="1" data-row="1" data-visible-time="1700723133176" data-largest-intersection-ratio="1">
                <a class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]" href="https://www.linkedin.com/jobs/view/software-engineer-at-works-3326240771?refId=CDfF3BXhv52%2FJAXxfr1HkA%3D%3D&amp;trackingId=GQONh6GjtZPZWLigkqGGdw%3D%3D&amp;position=1&amp;pageNum=0&amp;trk=public_jobs_jserp-result_search-card" data-tracking-control-name="public_jobs_jserp-result_search-card" data-tracking-client-ingraph="" data-tracking-will-navigate="">
                    <span class="sr-only">
                        Software Engineer
                    </span>
                </a>
                <div class="search-entity-media">
                    <img class="artdeco-entity-image artdeco-entity-image--square-4 lazy-loaded" data-ghost-classes="artdeco-entity-image--ghost" data-ghost-url="https://static.licdn.com/aero-v1/sc/h/9a9u41thxt325ucfh5z8ga4m8" alt="" aria-busy="false" src="https://media.licdn.com/dms/image/C560BAQHrdBpK0M0UFw/company-logo_100_100/0/1646301011054/officialworks_logo?e=2147483647&amp;v=beta&amp;t=QYIuronx-2pVC9vNvyEJ9MVDhnyp8wjJEz2HLDQcuEc">
                </div>
                <div class="base-search-card__info">
                    <h3 class="base-search-card__title">
                        Software Engineer
                    </h3>
                    <h4 class="base-search-card__subtitle">
                        <a class="hidden-nested-link" data-tracking-client-ingraph="" data-tracking-control-name="public_jobs_jserp-result_job-search-card-subtitle" data-tracking-will-navigate="" href="https://sg.linkedin.com/company/officialworks?trk=public_jobs_jserp-result_job-search-card-subtitle">
                            Works
                        </a>
                    </h4>
                    <div class="base-search-card__metadata">
                      <span class="job-search-card__location">
                        California, United States
                      </span>
                      <div class="job-search-card__benefits">
                        <div class="result-benefits">
                            <icon class="result-benefits__icon lazy-loaded" data-svg-class-name="result-benefits__icon-svg" aria-hidden="true" aria-busy="false"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" focusable="false" class="result-benefits__icon-svg lazy-loaded" aria-busy="false">
                                <path d="M14.7 10H17L11.5 18L8 14.5L9.3 13.2L11.2 15.1L14.7 10ZM20 3V19C20 20.7 18.7 22 17 22H7C5.3 22 4 20.7 4 19V3H9.7L10.2 2C10.6 1.4 11.2 1 12 1C12.7 1 13.4 1.4 13.8 2L14.3 3H20ZM18 5H15.4L16 6.1V7H8V6.1L8.6 5H6V19C6 19.6 6.4 20 7 20H17C17.6 20 18 19.6 18 19V5Z" fill="currentColor"></path>
                            </svg></icon>
                            <span class="result-benefits__text">
                                Be an early applicant
                           </span>
                        </div>
                      </div>
                      <time class="job-search-card__listdate--new" datetime="2023-11-23">
                        2 minutes ago
                      </time>
                    </div>
                </div>
            </div>
          </li>
          <li>
            <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card" data-entity-urn="urn:li:jobPosting:3326240772" data-search-id="CDfF3BXhv52/JAXxfr1HkA==" data-tracking-id="GQONh6GjtZPZWLigkqGGdw==" data-column="1" data-row="1" data-visible-time="1700723133176" data-largest-intersection-ratio="1">
                <a class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]" href="https://www.linkedin.com/jobs/view/software-engineer-at-works-3326240771?refId=CDfF3BXhv52%2FJAXxfr1HkA%3D%3D&amp;trackingId=GQONh6GjtZPZWLigkqGGdw%3D%3D&amp;position=1&amp;pageNum=0&amp;trk=public_jobs_jserp-result_search-card" data-tracking-control-name="public_jobs_jserp-result_search-card" data-tracking-client-ingraph="" data-tracking-will-navigate="">
                    <span class="sr-only">
                        Software Engineer
                    </span>
                </a>
                <div class="search-entity-media">
                    <img class="artdeco-entity-image artdeco-entity-image--square-4 lazy-loaded" data-ghost-classes="artdeco-entity-image--ghost" data-ghost-url="https://static.licdn.com/aero-v1/sc/h/9a9u41thxt325ucfh5z8ga4m8" alt="" aria-busy="false" src="https://media.licdn.com/dms/image/C560BAQHrdBpK0M0UFw/company-logo_100_100/0/1646301011054/officialworks_logo?e=2147483647&amp;v=beta&amp;t=QYIuronx-2pVC9vNvyEJ9MVDhnyp8wjJEz2HLDQcuEc">
                </div>
                <div class="base-search-card__info">
                    <h3 class="base-search-card__title">
                        Senior Software Engineer
                    </h3>
                    <h4 class="base-search-card__subtitle">
                        <a class="hidden-nested-link" data-tracking-client-ingraph="" data-tracking-control-name="public_jobs_jserp-result_job-search-card-subtitle" data-tracking-will-navigate="" href="https://sg.linkedin.com/company/officialworks?trk=public_jobs_jserp-result_job-search-card-subtitle">
                            Works
                        </a>
                    </h4>
                    <div class="base-search-card__metadata">
                      <span class="job-search-card__location">
                        California, United States
                      </span>
                      <div class="job-search-card__benefits">
                        <div class="result-benefits">
                            <icon class="result-benefits__icon lazy-loaded" data-svg-class-name="result-benefits__icon-svg" aria-hidden="true" aria-busy="false"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" focusable="false" class="result-benefits__icon-svg lazy-loaded" aria-busy="false">
                                <path d="M14.7 10H17L11.5 18L8 14.5L9.3 13.2L11.2 15.1L14.7 10ZM20 3V19C20 20.7 18.7 22 17 22H7C5.3 22 4 20.7 4 19V3H9.7L10.2 2C10.6 1.4 11.2 1 12 1C12.7 1 13.4 1.4 13.8 2L14.3 3H20ZM18 5H15.4L16 6.1V7H8V6.1L8.6 5H6V19C6 19.6 6.4 20 7 20H17C17.6 20 18 19.6 18 19V5Z" fill="currentColor"></path>
                            </svg></icon>
                            <span class="result-benefits__text">
                                Be an early applicant
                           </span>
                        </div>
                      </div>
                      <time class="job-search-card__listdate--new" datetime="2023-11-23">
                        2 minutes ago
                      </time>
                    </div>
                </div>
            </div>
          </li>
        </ul>
        """
        html = BeautifulSoup(html_doc, 'html.parser')
        filter_jobs(html)

        notification = '{base_command} -title Software Engineer -subtitle Works -message From LinkedIn -open https://www.linkedin.com/jobs/search/?currentJobId=3326240771'.format(base_command=base_command)
        honk = 'afplay honk.aiff'
        calls = [call(notification), call(honk)]
        mock_system.assert_has_calls(calls, any_order=False)


if __name__ == '__main__':
    unittest.main()
