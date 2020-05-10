@selenium_test_feature
Feature: Selenium test feature
  I want to use this template for my feature file

  @selenium_test_chrome
  Scenario: Selenium Chrome test scenario
    Given a Google Chrome window is open
      And the user navigates to "http://passcomptia.com/"
     Then the current window URL is "http://passcomptia.com/"

  @selenium_test_ie
  Scenario: Selenium IE test scenario
    Given an Internet Explorer window is open

  @selenium_test_firefox
  Scenario: Selenium Firefox test scenario
    Given a Mozilla Firefox window is open
