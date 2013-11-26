Feature: wages owed

    Scenario: capturing claimants unpaid wage details so that their claim can be processed by RPS
     Given the app is running
      When we visit /claim-redundancy-payment/wages-owed-details/
      Then the page should have title "Wages owed"
       And the page should have an input field called "owed" labeled "Are you owed any wages?"
       And the page should have an input field called "wage_owed_from" labeled "From"
       And the page should have an input field called "wage_owed_to" labeled "To"
       And the page should have an input field called "number_of_days_owed" labeled "Number of days for which pay is owed"
       And the page should have an input field called "gross_amount_owed" labeled "Gross amount of pay owed"
       And the page should not have a call to action box at the top of the screen

    Scenario: submit valid information
        Given a claimant with the unpaid wage details
            | DETAILS             | VALUE      |
            | owed                | Yes        |
            | wage_owed_from      | 01/04/2013 |
            | wage_owed_to        | 01/05/2013 |
            | number_of_days_owed | 1          |
            | gross_amount_owed   | 200.00     |
         When the claimant goes to /claim-redundancy-payment/wages-owed-details/
          And enters the unpaid wages details
         Then the claimant should be redirected

    Scenario: submit valid information with no wages owed
        Given a claimant with the unpaid wage details
            | DETAILS             | VALUE      |
            | owed                | No         |
         When the claimant goes to /claim-redundancy-payment/wages-owed-details/
          And enters the unpaid wages details
         Then the claimant should be redirected

    Scenario: mandatory fields check
        Given a claimant with the unpaid wage details
            | DETAILS             | VALUE      |
            | owed                | Yes        |
            | wage_owed_from      |            |
            | wage_owed_to        |            |
            | number_of_days_owed |            |
            | gross_amount_owed   | 2000       |
         When the claimant goes to /claim-redundancy-payment/wages-owed-details/
          And enters the unpaid wages details
         Then the claimant should stay on /wages-owed-details/ with title "Wages owed"


