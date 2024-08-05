/**
 * Created by oleg.perushko@symphony-solutions.eu on 25.04.16
 */
package com.egalacoral.utils;

import org.springframework.stereotype.Component;

import java.util.Map;

import etm.core.renderer.MeasurementRenderer;

@Component
public class EtmJoinPointService implements MeasurementRenderer, Runnable {
	@Override
	public void render(Map points) {

	}

	@Override
	public void run() {

	}
}
