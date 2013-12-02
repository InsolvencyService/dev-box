Feature: Chomp

  @nuke_db
  @chomp
  Scenario: getting the next claim to be put into chomp
    Given a claim exists
    When we ask for the next claim
    Then we are redirected to the next claim
    And that claim's status is In Progress

  @nuke_db
  @chomp
  Scenario: setting the state of a claim
    Given a claim is in In Progress
    When we set the state to Done
    Then the state is Done

  @nuke_db
  @chomp
  Scenario: getting an acceptdoc
    Given a claim is in In Progress
    Then we can get the acceptdoc

  @nuke_db
  @chomp
  Scenario: getting an rp1
    Given a claim is in In Progress
    Then we can get the rp1

  @nuke_db
  @chomp
  Scenario: getting an rp14
    Given a claim is in In Progress
    Then we can get the rp14

  @nuke_db
  @chomp
  Scenario: getting an rp14a
    Given a claim is in In Progress
    Then we can get the rp14a
