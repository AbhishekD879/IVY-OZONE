/**
 * Created by oleg.perushko@symphony-solutions.eu on 25.04.16
 */
package com.egalacoral.component;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.CacheLoader;
import com.google.common.cache.LoadingCache;

import com.egalacoral.api.siteserv.SSResponse;
import com.egalacoral.utils.LoggingRESTRequestInterceptor;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.converter.FormHttpMessageConverter;
import org.springframework.http.converter.StringHttpMessageConverter;
import org.springframework.http.converter.xml.MarshallingHttpMessageConverter;
import org.springframework.oxm.jaxb.Jaxb2Marshaller;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.Collections;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

import javax.annotation.PostConstruct;

@Component
public class SiteServService extends RestTemplate {

//	@Qualifier("siteServService")
//	private @Autowired Jaxb2Marshaller jaxb2Marshaller;

//	@Value("${bet-placement.url}")
	private String url;

	private LoadingCache<String, SSResponse> loadingCache = CacheBuilder.newBuilder()
			.maximumSize(100_000)
			.expireAfterWrite(5, TimeUnit.SECONDS)
			.build(new CacheLoader<String, SSResponse>() {
				@Override
				public SSResponse load(String key) throws Exception {
					return uncachedRequest(key);
				}
			});

	@PostConstruct
	public void setup() {
		final MarshallingHttpMessageConverter marshallingHttpMessageConverter = new MarshallingHttpMessageConverter();
//		marshallingHttpMessageConverter.setMarshaller(jaxb2Marshaller);
//		marshallingHttpMessageConverter.setUnmarshaller(jaxb2Marshaller);
		setMessageConverters(Arrays.asList(
				marshallingHttpMessageConverter,
				new FormHttpMessageConverter(),
				new StringHttpMessageConverter())
		);
		setInterceptors(Collections.singletonList(new LoggingRESTRequestInterceptor()));
	}

	public SSResponse request(String resource) {
		try {
			return loadingCache.get(resource);
		} catch (ExecutionException e) {
			e.printStackTrace();
			return uncachedRequest(resource);
		}
	}

	private SSResponse uncachedRequest(String resource) {
		return this.getForObject(url + resource + "?translationLang=en", SSResponse.class);
	}
}
