Feature: form navigation

    Scenario: navigation between form pages and storing information
        Given the form pages
            | PAGE                                          |
            | /claim-redundancy-payment/employment-details/ |
            | /claim-redundancy-payment/summary/            |
            | /claim-redundancy-payment/wage-details/       |
            | /claim-redundancy-payment/summary/            |
         When visiting each form page
         Then we should see a navigation bar with these links
            | LINK                                          |
            | /claim-redundancy-payment/personal-details/   |
            | /claim-redundancy-payment/employment-details/ |
            | /claim-redundancy-payment/wage-details/       |
