= Architecting Serverless Microservices on the Cloud with AWS

How to generate the HTML page with the workshop notes:

* Install the `asciidoctor` and `pygments.rb` Ruby gems. At the terminal type:

        gem install asciidoctor pygments.rb 

* Move to the `docs` directory.

        cd docs

* Run `asciidoctor` on the `microservices.adoc` file:
 
        asciidoctor microservices.adoc

The resulting file is: `microservices.html`.
