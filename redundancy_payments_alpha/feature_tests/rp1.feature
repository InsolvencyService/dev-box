@jims
Feature: rp1 form

    Scenario: adding rp1 form details to data store
        When we add a dictionary containing sample rp1 details
        Then the data store should contain a claimant
        And the chomp service should generate an xml payload containing Donald