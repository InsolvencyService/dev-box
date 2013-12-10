Feature: gross rate of pay calculator

    Scenario: calculating weekly gross rate of pay from yearly gross rate of pay
        Given a claimant who gets paid 25000 pounds a year fills out the calculator
         When their gross rate of pay is calculated
         Then the weekly gross rate of pay returned should be 479.45 pounds
          And the wage details page should have gross rate of pay prepopulated


    Scenario: calculating weekly gross rate of pay from weekly gross rate of pay
        Given a claimant who gets paid 700 pounds a week fills out the calculator
         When their gross rate of pay is calculated
         Then the weekly gross rate of pay returned should be 700 pounds 
          And the wage details page should have gross rate of pay prepopulated

