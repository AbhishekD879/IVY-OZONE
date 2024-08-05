package com.coral.inplay;

import static spark.Spark.*;

/**
 * Created by oleg.perushko@symphony-solutions.eu on 02.02.16.
 */
public class Service {
    public static void main(String[] args) {
        get("/sports", (request, response) -> null);
        get("/events", (request, response) -> null);
    }
}
