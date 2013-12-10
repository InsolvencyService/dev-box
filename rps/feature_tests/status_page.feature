Feature: app status page

    Scenario: check that the app is running
        Given the app is running
         When we visit /_status
         Then the page should include "everything is ok"

