/**
 * Created by oleg.perushko@symphony-solutions.eu on 10.05.16
 */

package com.egalacoral.configuration;

import com.egalacoral.component.SimpleHandler;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WeSocketConfig implements WebSocketConfigurer {

	@Override
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(simpleHandler(), "/betslip").withSockJS();
	}

	@Bean
	public WebSocketHandler simpleHandler() {
		return new SimpleHandler();
	}
}
