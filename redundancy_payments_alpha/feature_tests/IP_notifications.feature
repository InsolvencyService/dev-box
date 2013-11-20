# Story: IP email notifications
#
# As an: IP
# I want: to receive email notifications when a claim is submitted
# So that: I can review the current status of the claim

@wip
Feature: send email notification to IP

    Scenario: sending a notification email
        Given the claimant has submitted a claim
         When the notifications are triggered
         Then the email is sent to the IP
