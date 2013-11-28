# Story: Leena-tron
#
# As an: Leena-tron
# I want: to see claims that were submitted
# So that: I can post the xml to CHAMP

@wip
Feature: get messages from the queue

    Scenario: submitting a claim results in a message on the queue
        Given the claimant has created a claim
         When the claimant submits the claim
         Then the queue should have the claim on it

