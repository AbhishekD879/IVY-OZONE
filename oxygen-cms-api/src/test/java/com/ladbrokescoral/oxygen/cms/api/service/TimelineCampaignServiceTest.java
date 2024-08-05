package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus.*;
import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.ChangeCampaignTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.timeline.RemoveCampaignTimelineMessageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Campaign;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineCampaignRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
public class TimelineCampaignServiceTest extends BDDMockito {

  public static final String CAMPAIGN_ID = "2342243";
  private static final String BRAND = "ladbrokes";
  private static final String BMA = "bma";

  private Campaign campaign;
  private Campaign existingCampaign;

  @Mock TimelineCampaignRepository repository;
  @Mock TimelinePostService postService;
  @Mock TimelineKafkaPublisher timelineKafkaPublisher;

  @InjectMocks private TimelineCampaignService service;

  @Before
  public void setUp() {

    campaign = new Campaign();
    campaign.setName("testCampaign");
    campaign.setDisplayFrom(Instant.now());
    campaign.setDisplayTo(Instant.now().plusSeconds(60 * 60 * 24 * 3));
    campaign.setStatus(LIVE);
    campaign.setCreatedAt(Instant.now());
    campaign.setBrand(BRAND);

    existingCampaign = new Campaign();
    existingCampaign.setId(CAMPAIGN_ID);
    existingCampaign.setName("ExistingCampaign");
    existingCampaign.setDisplayFrom(Instant.now());
    existingCampaign.setDisplayTo(Instant.now().plusSeconds(60 * 60 * 24 * 7));

    doAnswer((Answer<Void>) invocation -> null).when(postService).delete(anyString());
    when(repository.save(campaign)).thenReturn(campaign);
  }

  @Test(expected = ValidationException.class)
  public void testValidationExceptionThrownOnHavingCrossingCampaign() {
    when(repository.findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(any(), any(), any(), any()))
        .thenReturn(Optional.of(new Campaign()));

    service.save(campaign);

    verify(repository, times(0)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(0)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignSavedAndMessageSendToKafkaIfValidAndStatusLive() {
    when(repository.findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(any(), any(), any(), any()))
        .thenReturn(Optional.empty());
    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());
    service.save(campaign);

    verify(repository, times(1)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(1)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignSavedAndMessageNotSendToKafkaIfValidAndStatusNotLive() {

    campaign.setStatus(OPEN);

    service.save(campaign);

    verify(repository, times(1)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(0)).publishTimelineMessage(any(), any());
  }

  @Test(expected = ValidationException.class)
  public void testValidationExceptionThrownOnHavingCrossingCampaignOnUpdate() {
    when(repository.findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(any(), any(), any(), any()))
        .thenReturn(Optional.of(new Campaign()));

    service.update(existingCampaign, campaign);

    verify(repository, times(0)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(0)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignUpdatedAndMessageSendToKafkaIfValidAndStatusLive() {
    campaign.setStatus(LIVE);
    when(repository.findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(any(), any(), any(), any()))
        .thenReturn(Optional.empty());
    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());

    service.update(existingCampaign, campaign);

    verify(repository, times(1)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(1)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignUpdatedAndMessageNotSendToKafkaIfValidAndStatusLive() {

    existingCampaign.setStatus(OPEN);
    campaign.setStatus(OPEN);

    service.update(existingCampaign, campaign);

    verify(repository, times(1)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(0)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignUpdatedAndMessageSendToKafkaIfValidAndStatusClosed() {
    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());
    existingCampaign.setStatus(LIVE);
    existingCampaign.setDisplayTo(Instant.now().plus(Duration.ofDays(3)));

    campaign.setStatus(CLOSED);
    campaign.setId(CAMPAIGN_ID);

    service.update(existingCampaign, campaign);

    ArgumentCaptor<RemoveCampaignTimelineMessageDto> removeMessage =
        ArgumentCaptor.forClass(RemoveCampaignTimelineMessageDto.class);
    verify(repository, times(1)).save(any(Campaign.class));
    verify(timelineKafkaPublisher, times(1)).publishTimelineMessage(any(), removeMessage.capture());
    assertNotNull(removeMessage.getValue().getId());
    assertNotNull(removeMessage.getValue().getAffectedMessageId());
    assertNotNull(removeMessage.getValue().getCreatedDate());
  }

  @Test
  public void testLiveCampaignUpdatedAndMessageSendToKafka() {
    existingCampaign.setStatus(LIVE);
    campaign.setId(CAMPAIGN_ID);
    campaign.setStatus(LIVE);
    when(repository.findByIdIsNotAndBrandAndStatusAndDisplayToIsAfter(any(), any(), any(), any()))
        .thenReturn(Optional.empty());

    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());

    service.update(existingCampaign, campaign);

    ArgumentCaptor<ChangeCampaignTimelineMessageDto> changeMessage =
        ArgumentCaptor.forClass(ChangeCampaignTimelineMessageDto.class);

    verify(repository, times(1)).save(any(Campaign.class));

    verify(timelineKafkaPublisher, times(1)).publishTimelineMessage(any(), changeMessage.capture());
    assertNotNull(changeMessage.getValue().getData());
    assertNotNull(changeMessage.getValue().getId());
    assertNotNull(changeMessage.getValue().getAffectedMessageId());
    assertNotNull(changeMessage.getValue().getCreatedDate());
  }

  @Test
  public void testCampaignDeleting() {
    when(repository.findById(anyString())).thenReturn(Optional.of(campaign));
    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());
    campaign.setPostsIds(Arrays.asList("1", "2"));
    campaign.setStatus(LIVE);

    service.delete(CAMPAIGN_ID);

    verify(postService, times(2)).delete(anyString());
    verify(repository).deleteById(anyString());
    verify(timelineKafkaPublisher).publishTimelineMessage(any(), any());
  }

  @Test
  public void testCampaignDeletingBMA() {
    when(repository.findById(anyString())).thenReturn(Optional.of(campaign));
    doNothing().when(timelineKafkaPublisher).publishTimelineMessage(any(), any());
    campaign.setPostsIds(Arrays.asList("1", "2"));
    campaign.setStatus(LIVE);
    campaign.setBrand(BMA);

    service.delete(CAMPAIGN_ID);

    verify(postService, times(2)).delete(anyString());
    verify(repository).deleteById(anyString());
    verify(timelineKafkaPublisher).publishTimelineMessage(any(), any());
  }

  @Test
  public void testNotLiveCampaignDeleting() {
    when(repository.findById(anyString())).thenReturn(Optional.of(campaign));
    campaign.setStatus(OPEN);

    service.delete(CAMPAIGN_ID);

    verify(repository).deleteById(anyString());
    verify(timelineKafkaPublisher, times(0)).publishTimelineMessage(any(), any());
  }

  @Test
  public void testFindByBrandOrdered() {
    Sort sort = Sort.by(Sort.Order.by("updatedAt"));

    service.findByBrandOrdered(BRAND, sort);

    verify(repository).findByBrand(BRAND, sort);
  }

  @Test
  public void testFindCurrentLiveCampaignByBrand() {
    service.findCurrentLiveCampaignByBrand(CAMPAIGN_ID);

    verify(repository).findCurrentLiveCampaignByBrand(anyString(), any(Instant.class));
  }
}
