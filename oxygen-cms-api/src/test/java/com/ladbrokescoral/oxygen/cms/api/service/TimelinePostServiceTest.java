package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.*;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelinePostPageRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.time.Instant;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.AdditionalAnswers;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
public class TimelinePostServiceTest extends BDDMockito {

  public static final String POST_ID = "3454332234";
  public static final String CAMPAIGN_ID = "234434323";

  private TimelinePostService service;

  @Mock private TimelinePostPageRepository repository;
  @Mock private TimelineCampaignService campaignService;
  @Mock private TimelineKafkaPublisher timelineKafkaPublisher;

  TimelinePost post;
  Campaign campaign;

  @Before
  public void setUp() {
    post = new TimelinePost();
    post.setId(POST_ID);
    post.setBrand("bma");
    campaign = new Campaign();
    campaign.setId(CAMPAIGN_ID);
    campaign.setName("testCampaign");
    campaign.setStatus(CampaignStatus.LIVE);
    campaign.setDisplayFrom(Instant.now().minusSeconds(60 * 60 * 24 * 3));
    campaign.setDisplayTo(Instant.now().plusSeconds(60 * 60 * 24 * 3));
    campaign.setCreatedAt(Instant.now());
    campaign.setBrand("bma");

    service = new TimelinePostService(repository, campaignService, timelineKafkaPublisher);

    given(repository.save(any(TimelinePost.class))).will(AdditionalAnswers.returnsFirstArg());
    given(campaignService.findOne(any())).willReturn(Optional.of(campaign));
  }

  @Test
  public void testFindByBrandAndCampaignId() {
    Sort sort = Sort.by("field1");
    service.findByBrandAndCampaignId("bma", "2433456533", sort);

    verify(repository).findByBrandAndCampaignId("bma", "2433456533", sort);
  }

  @Test
  public void testFindByBrandAndCampaignIdPaginated() {
    Sort sort = Sort.by("updatedAt");
    Pageable pageable = PageRequest.of(0, 3, sort);
    service.findPageByBrandAndCampaignId("bma", "2433456533", pageable);

    verify(repository).findPageByBrandAndCampaignId("bma", "2433456533", pageable);
  }

  @Test
  public void testGetCountByBrandAndCampaignId() {
    service.getCountByBrandAndCampaignId("bma", "2433456533");

    verify(repository).countByBrandAndCampaignId("bma", "2433456533");
  }

  @Test
  public void testSaveDraftPost() {
    post.setPostStatus(PostStatus.DRAFT);

    service.save(post);

    verify(repository).save(post);
    verify(campaignService, times(0)).findOne(any());
  }

  @Test
  public void testSavePublishedPost() {
    post.setPostStatus(PostStatus.PUBLISHED);

    service.save(post);

    verify(campaignService).findOne(any());
    verify(repository).save(post);
  }

  @Test(expected = NotFoundException.class)
  public void testSavePublishedPostForUnexistingCampaign() {
    when(campaignService.findOne(any())).thenReturn(Optional.empty());
    post.setPostStatus(PostStatus.PUBLISHED);

    service.save(post);

    verify(campaignService).findOne(any());
    verify(repository).save(post);
  }

  @Test(expected = ValidationException.class)
  public void testSavePublishedPostForFutureCampaign() {
    post.setPostStatus(PostStatus.PUBLISHED);
    campaign.setDisplayFrom(Instant.now().plusSeconds(1000));
    campaign.setDisplayTo(Instant.now().plusSeconds(10000));

    service.save(post);

    verify(campaignService).findOne(any());
    verify(repository, times(0)).save(post);
  }

  @Test(expected = ValidationException.class)
  public void testSavePublishedPostForPreviousCampaign() {
    post.setPostStatus(PostStatus.PUBLISHED);
    campaign.setDisplayFrom(Instant.now().minusSeconds(10000));
    campaign.setDisplayTo(Instant.now().minusSeconds(1000));

    service.save(post);

    verify(campaignService).findOne(any());
    verify(repository, times(0)).save(post);
  }

  @Test
  public void testDelete() {
    when(repository.findById(any())).thenReturn(Optional.of(post));

    service.delete(POST_ID);

    verify(repository).deleteById(anyString());
  }

  @Test
  public void testPostPublishingUpdate() {
    TimelinePost updatedPost = new TimelinePost();
    updatedPost.setId(POST_ID);
    updatedPost.setPostStatus(PostStatus.PUBLISHED);
    post.setPostStatus(PostStatus.DRAFT);
    updatedPost.setBrand("bma");
    service.update(post, updatedPost);

    assertNotNull(updatedPost.getPublishedAt());
    verify(repository).save(updatedPost);
  }

  @Test
  public void testPostUnpublishingUpdate() {
    Instant publishedAt = Instant.now();
    post.setPublishedAt(publishedAt);
    post.setPostStatus(PostStatus.PUBLISHED);
    TimelinePost updatedPost = new TimelinePost();
    updatedPost.setId(POST_ID);
    updatedPost.setPublishedAt(publishedAt);
    updatedPost.setPostStatus(PostStatus.UNPUBLISHED);
    updatedPost.setBrand("bma");
    service.update(post, updatedPost);

    verify(repository).save(updatedPost);
  }

  @Test
  public void testPublishedPostModificationUpdate() {
    Instant publishedAt = Instant.now();
    post.setPublishedAt(publishedAt);
    post.setPostStatus(PostStatus.PUBLISHED);
    post.setTemplate(new Template());

    TimelinePost updatedPost = new TimelinePost();
    updatedPost.setId(POST_ID);
    updatedPost.setPublishedAt(publishedAt);
    updatedPost.setPostStatus(PostStatus.PUBLISHED);
    updatedPost.setTemplate(new Template());
    updatedPost.getTemplate().setHeaderText("header");
    updatedPost.setBrand("bma");

    service.update(post, updatedPost);

    verify(repository).save(updatedPost);
  }

  @Test
  public void testUnpublishedPostUpdate() {
    Instant publishedAt = Instant.now();
    post.setPublishedAt(publishedAt);
    post.setPostStatus(PostStatus.UNPUBLISHED);
    post.setTemplate(new Template());

    TimelinePost updatedPost = new TimelinePost();
    updatedPost.setId(POST_ID);
    updatedPost.setPublishedAt(publishedAt);
    updatedPost.setPostStatus(PostStatus.UNPUBLISHED);
    updatedPost.setTemplate(new Template());
    updatedPost.getTemplate().setHeaderText("header");

    service.update(post, updatedPost);

    verify(repository).save(updatedPost);
  }
}
