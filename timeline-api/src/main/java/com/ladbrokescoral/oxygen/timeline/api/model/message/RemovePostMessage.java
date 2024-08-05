package com.ladbrokescoral.oxygen.timeline.api.model.message;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import org.springframework.data.redis.core.RedisHash;

@RedisHash
@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public class RemovePostMessage extends ActionMessage {}
