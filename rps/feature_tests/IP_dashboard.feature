Feature: IP dashboard

    Scenario: viewing an empty dashboard
        Given the IP app is running
         When we visit /ip-dashboard/claims/
         Then the page should have title "Insolvency Practitioners - Redundancy Payments - The Insolvency Service"
          And the page should have text "No claims"

    Scenario: viewing a dashboard with claims
        Given the IP app is running
          And there are claims in the database
         When we visit /ip-dashboard/claims/
         Then the page should have title "Insolvency Practitioners - Redundancy Payments - The Insolvency Service"
          And the page should have text "23/05/1982"
          And the page should have text "XX223344X"
          And the page should have text "Jones"
          And the page should have text "T R M"
          And the page should have text that is the current date
