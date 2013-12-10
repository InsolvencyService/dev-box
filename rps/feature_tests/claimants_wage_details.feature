Feature: claimants wage details

    Scenario: capturing claimants wage details so that ..
        Given the app is running
         When we visit /claim-redundancy-payment/wage-details/
         Then the page should have title "Claimant Wage Details"
           And the page should have an input field called "gross_rate_of_pay" labeled "Gross rate of pay per week (before Tax and NI, excluding overtime)"
           And the page should have an input field called "number_of_hours_worked" labeled "Number of hours you normally worked per week"
           And the page should have an input field called "bonus_or_commission" labeled "Did your pay include any bonus or commission ?"
           And the page should have an input field called "overtime" labeled "Did you work overtime as a part of your contract ?"
           And the page should have an input field called "hours_of_overtime" labeled "How many hours overtime did you normally work?"
           And the page should have an input field called "normal_days_of_work" labeled "How many days did you normally work each week?"
           And the page should have an input field called "bonus_details" labeled "Give details of the amount and type of bonus or commission earned, and when it was paid"
           And the page should not have a call to action box at the top of the screen


    Scenario: conditional mandatory overtime field check
        Given a claimant with the wages details
            | DETAILS               | VALUE      |
            | gross_rate_of_pay     | 100        |
            | frequency_of_payment  | week       |
            | number_of_hours_worked| 35         |
            | bonus_or_commission   | Yes        |
            | overtime              | Yes        |
            | hours_of_overtime     |            |
            | normal_days_of_work   | 5          |
            | bonus_details         | 50          |
         When the claimant goes to /claim-redundancy-payment/wage-details/
          And enters the wages details
         Then the claimant should stay on /wage-details/ with title "Claimant Wage Details"
