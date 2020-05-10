@rest_feature_test
Feature: REST Services Feature Test
  Just a test.

  @rest_get_test
  Scenario: REST Single Scenario Test
    Given all GET Requests are successfully executed against the data table
      | url                     |
      | http://www.facebook.com |

  @rest_put_test
  Scenario Outline: REST Multiple Scenario Test
    Given a GET REST request is sent to the following URL table data
      | url   |
      | <url> |

    Examples: <url>
      | url             | 
      | www.myspace.com |
      | name2           |
