package com.egalacoral.spark.timeform.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Configuration
public class SwaggerDocumentationConfiguration {

  ApiInfo apiInfo() {
    return new ApiInfoBuilder()
        .title("SPARK-Timeform RESTful API")
        .description(
            "RESTfull API for tracking informaton about greyhound and horce races. Version 1.0.1")
        .license("")
        .licenseUrl("")
        .termsOfServiceUrl("")
        .version("1.0.1")
        .contact(new Contact("", "", ""))
        .build();
  }

  @Bean
  public Docket customImplementation() {
    return new Docket(DocumentationType.SWAGGER_2)
        .select()
        .apis(RequestHandlerSelectors.basePackage("com.egalacoral.spark.timeform.controller.api"))
        .build()
        .directModelSubstitute(org.joda.time.LocalDate.class, java.sql.Date.class)
        .directModelSubstitute(org.joda.time.DateTime.class, java.util.Date.class)
        .apiInfo(apiInfo());
  }
}
