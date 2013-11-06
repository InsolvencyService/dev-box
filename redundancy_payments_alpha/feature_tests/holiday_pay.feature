@wip
Feature: claimants holiday pay

    Scenario: capturing claimants holiday pay details so that their claim can be processed by RPS
     Given the app is running
      When we visit /claim-redundancy-payment/holiday-pay/
       Then the page should have title "Holiday pay"
        And the page should have an input field called "holiday_owed" labeled "Are you owed any holiday pay?"
        And the page should have an input field called "holiday_start_date" labeled "What was the start date of your holiday year?"
        And the page should have an input field called "number_of_holiday_days_entitled" labeled "How many days holiday per year (including bank holidays) were you entitled to?"
        And the page should have an input field called "days_carried_over" labeled "If you were allowed to carry forward untaken holiday entitlement from your previous holiday year, how many days did you carry forward this year?"
        And the page should have an input field called "days_taken" labeled "How many days have you taken this year (including bank holidays)?"
        And the page should have an input field called "days_owed" labeled "How many days are you still owed (including bank holidays) up to your termination date?"
        And the page should have an input field called "holiday_taken_from" labeled "From"
        And the page should have an input field called "holiday_taken_to" labeled "To"
        And the page should have an input field called "number_of_days_pay_owed" labeled "Number of days for which pay is owed"

    Scenario: Submit valid information
     Given a claimant with the holiday pay details
       | DETAILS                         | VALUE      |
       | holiday_owed                    | Yes        |
       | holiday_start_date              | 01/04/2013 |
       | number_of_holiday_days_entitled | 5          |
       | days_carried_over               | 15         |
       | days_taken                      | 10         |
       | days_owed                       | 5          |
      When the claimant goes to /claim-redundancy-payment/holiday-pay/
          And enters the holiday pay details
      Then the claimant should be redirected

    Scenario: Submit holiday owed with missing required information
     Given a claimant with the holiday pay details
       | DETAILS                         | VALUE      |
       | holiday_owed                    | Yes        |
       | holiday_start_date              | 01/04/2013 |
       | number_of_holiday_days_entitled | 5          |
       | days_carried_over               | 15         |
      When the claimant goes to /claim-redundancy-payment/holiday-pay/
          And enters the holiday pay details
      Then the claimant should stay on /claim-redundancy-payment/holiday-pay/ with title "Holiday pay"
      And the form should display error message "Days taken mandatory fields has not been completed"
      And the form should display error message "Days owed mandatory fields has not been completed"
