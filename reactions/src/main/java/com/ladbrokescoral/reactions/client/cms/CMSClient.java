package com.ladbrokescoral.reactions.client.cms;

import com.fasterxml.jackson.databind.JsonNode;
import java.util.List;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 15-06-2023
 */
public interface CMSClient {

  Mono<List<String>> getActiveSelectionIdAndSurfaceBetIdKeys();

  Mono<JsonNode> getCmsHealth();
}
