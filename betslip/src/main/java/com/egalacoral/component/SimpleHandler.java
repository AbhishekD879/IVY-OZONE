/**
 * Created by oleg.perushko@symphony-solutions.eu on 15.05.16
 */

package com.egalacoral.component;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

public class SimpleHandler extends TextWebSocketHandler {

	@Override
	protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
		Thread.sleep(1_000);
		TextMessage textMessage = new TextMessage("Hello, " + message.getPayload() + "!");
		session.sendMessage(textMessage);
	}
}
