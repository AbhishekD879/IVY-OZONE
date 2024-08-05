/**
 * Created by oleg.perushko@symphony-solutions.eu on 26.04.16
 */

package com.egalacoral.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.client.ClientHttpRequestExecution;
import org.springframework.http.client.ClientHttpRequestInterceptor;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.util.StreamUtils;

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.stream.Collectors;

public class LoggingRESTRequestInterceptor implements ClientHttpRequestInterceptor {

	private static final Logger logger = LoggerFactory.getLogger("TRAFFIC: ");

	@Override
	public ClientHttpResponse intercept(HttpRequest request, byte[] body, ClientHttpRequestExecution execution)
			throws IOException {
		traceRequest(request, body);
		ClientHttpResponse response = execution.execute(request, body);
		BufferingClientHttpResponseWrapper wrapper = new BufferingClientHttpResponseWrapper(response);
		traceResponse(wrapper);
		return wrapper;
	}

	private void traceRequest(HttpRequest request, byte[] body) throws UnsupportedEncodingException {
		logger.info(request.getURI().toASCIIString());
	}

	private void traceResponse(ClientHttpResponse response) throws IOException {
		InputStream is = response.getBody();
		if (is != null) {
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			logger.info(reader.lines().collect(Collectors.joining("\n")).replace("\n", ""));
		} else {
			logger.info(response.getStatusText().replace("\n", ""));
		}
	}

	class BufferingClientHttpResponseWrapper implements ClientHttpResponse {

		private final ClientHttpResponse response;
		private byte[] body;

		BufferingClientHttpResponseWrapper(ClientHttpResponse response) {
			this.response = response;
		}

		@Override
		public HttpStatus getStatusCode() throws IOException {
			return this.response.getStatusCode();
		}

		@Override
		public int getRawStatusCode() throws IOException {
			return this.response.getRawStatusCode();
		}

		@Override
		public String getStatusText() throws IOException {
			return this.response.getStatusText();
		}

		@Override
		public HttpHeaders getHeaders() {
			return this.response.getHeaders();
		}

		@Override
		public InputStream getBody() throws IOException {
			if (this.body == null) {
				if (this.response.getBody() != null) {
					this.body = StreamUtils.copyToByteArray(this.response.getBody());
				} else {
					return null;
				}
			}
			return new ByteArrayInputStream(this.body);
		}

		@Override
		public void close() {
			this.response.close();
		}
	}
}
