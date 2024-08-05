/**
 * Created by oleg.perushko@symphony-solutions.eu on 02.03.16
 */

package com.egalacoral.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ws.client.WebServiceClientException;
import org.springframework.ws.client.WebServiceIOException;
import org.springframework.ws.client.support.interceptor.ClientInterceptor;
import org.springframework.ws.context.MessageContext;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class LoggingRequestInterceptor implements ClientInterceptor {

	private static final Logger reqLogger = LoggerFactory.getLogger("REQUEST");
	private static final Logger resLogger = LoggerFactory.getLogger("RESPONSE");

	@Override
	public boolean handleRequest(MessageContext messageContext) throws WebServiceClientException {
		ByteArrayOutputStream os = new ByteArrayOutputStream();
		try {
			messageContext.getRequest().writeTo(os);
		} catch (IOException e) {
			throw new WebServiceIOException(e.getMessage(), e);
		}

		String request = new String(os.toByteArray());
		reqLogger.info(request);
		return true;
	}

	@Override
	public boolean handleResponse(MessageContext messageContext) throws WebServiceClientException {
		ByteArrayOutputStream os = new ByteArrayOutputStream();
		try {
			messageContext.getResponse().writeTo(os);
		} catch (IOException e) {
			throw new WebServiceIOException(e.getMessage(), e);
		}

		String response = new String(os.toByteArray());
		resLogger.info(response);
		return true;
	}

	@Override
	public boolean handleFault(MessageContext messageContext) throws WebServiceClientException {
		ByteArrayOutputStream os = new ByteArrayOutputStream();
		try {
			messageContext.getResponse().writeTo(os);
		} catch (IOException e) {
			throw new WebServiceIOException(e.getMessage(), e);
		}

		String response = new String(os.toByteArray());
		resLogger.info("Fault Envelope: " + response);
		return false;
	}

	@Override
	public void afterCompletion(MessageContext messageContext, Exception ex) throws WebServiceClientException {

	}
}

