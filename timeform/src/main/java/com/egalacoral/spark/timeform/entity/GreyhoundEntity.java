package com.egalacoral.spark.timeform.entity;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBAttribute;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBHashKey;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTable;
import java.io.Serializable;
import java.util.List;

@DynamoDBTable(tableName = "greyhound")
public class GreyhoundEntity implements Serializable {
  @DynamoDBHashKey private Integer greyhoundId;
  @DynamoDBAttribute private String lastUpdate;
  private List<PositionEntity> positionEntities;

  public Integer getGreyhoundId() {
    return greyhoundId;
  }

  public void setGreyhoundId(Integer greyhoundId) {
    this.greyhoundId = greyhoundId;
  }

  public String getLastUpdate() {
    return lastUpdate;
  }

  public void setLastUpdate(String lastUpdate) {
    this.lastUpdate = lastUpdate;
  }

  public List<PositionEntity> getPositionEntities() {
    return positionEntities;
  }

  public void setPositionEntities(List<PositionEntity> positionEntities) {
    this.positionEntities = positionEntities;
  }

  public static final class GreyhoundEntityBuilder {
    private Integer greyhoundId;
    private String lastUpdate;
    private List<PositionEntity> positionEntities;

    private GreyhoundEntityBuilder() {}

    public static GreyhoundEntityBuilder aGreyhoundEntity() {
      return new GreyhoundEntityBuilder();
    }

    public GreyhoundEntityBuilder greyhoundId(Integer greyhoundId) {
      this.greyhoundId = greyhoundId;
      return this;
    }

    public GreyhoundEntityBuilder lastUpdate(String lastUpdate) {
      this.lastUpdate = lastUpdate;
      return this;
    }

    public GreyhoundEntityBuilder positionEntities(List<PositionEntity> positionEntities) {
      this.positionEntities = positionEntities;
      return this;
    }

    public GreyhoundEntity build() {
      GreyhoundEntity greyhoundEntity = new GreyhoundEntity();
      greyhoundEntity.setGreyhoundId(greyhoundId);
      greyhoundEntity.setLastUpdate(lastUpdate);
      greyhoundEntity.setPositionEntities(positionEntities);
      return greyhoundEntity;
    }
  }
}
