@ip_dashboard
Feature: IP dashboard

    Scenario: viewing an empty dashboard
        Given the IP app is running
         When we visit /ip-dashboard/claims/
         Then the page should have title "IP Dashboard"
          And the page should have text "No claims"

    Scenario: viewing a dashboard with claims
        Given the IP app is running
          And there are claims in the database
         When we visit /ip-dashboard/claims/
         Then the page should have title "IP Dashboard"
          And the page should have text "True"
          And the page should have text "False"
