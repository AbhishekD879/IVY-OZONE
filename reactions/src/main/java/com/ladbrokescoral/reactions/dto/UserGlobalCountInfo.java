package com.ladbrokescoral.reactions.dto;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * @author PBalarangakumar 14-06-2023
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record UserGlobalCountInfo(
    Long reaction1_globalCount,
    Long reaction2_globalCount,
    Long reaction3_globalCount,
    String userReaction) {}
