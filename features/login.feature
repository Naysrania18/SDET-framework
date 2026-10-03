Feature: Login
  As a fund operations user I want to log in so that I can see products

  @ui @bdd
  Scenario: Valid user logs in
    Given I am on the login page
    When I log in as "standard_user" with password "secret_sauce"
    Then I should see the "Products" page

  @ui @bdd
  Scenario: Locked out user is rejected
    Given I am on the login page
    When I log in as "locked_out_user" with password "secret_sauce"
    Then I should see the error "locked out"
