Feature: Robots.txt

    Scenario: Robots.txt should disallow everything
     Given the app is running
      When we visit /robots.txt
       Then the page should include "User-agent: *"
        And the page should include "Disallow: /"
