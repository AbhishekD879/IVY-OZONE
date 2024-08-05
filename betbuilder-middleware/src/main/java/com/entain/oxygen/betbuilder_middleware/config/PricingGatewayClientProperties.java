package com.entain.oxygen.betbuilder_middleware.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "pricing-gateway.httpclient")
public class PricingGatewayClientProperties extends WebClientProperties {}
