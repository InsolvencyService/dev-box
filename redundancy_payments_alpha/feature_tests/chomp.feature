Feature: Chomp

  @chomp
  Scenario: getting the next claim to be put into chomp
    Given a claim exists
    When we ask for the next claim
    Then we are redirected to the next claim
    And that claim's status is In Progress
