Feature: Users API

  @api @bdd
  Scenario: Fetch an existing user
    When I request user 3
    Then the response status is 200
    And the user id is 3
