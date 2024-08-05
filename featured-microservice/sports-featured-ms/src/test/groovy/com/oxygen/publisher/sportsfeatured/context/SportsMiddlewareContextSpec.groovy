package com.oxygen.publisher.sportsfeatured.context

import com.corundumstudio.socketio.Configuration
import com.corundumstudio.socketio.SocketIOServer
import com.oxygen.publisher.SocketIoTestHelper
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData
import com.oxygen.publisher.sportsfeatured.service.FeaturedServiceImpl
import spock.lang.Specification

class SportsMiddlewareContextSpec extends Specification{

  private SportsMiddlewareContext middlewareContext
  private SportsCachedData sportsCachedData
  private SportsServiceRegistry serviceRegistry

  void setup() {
    sportsCachedData = new SportsCachedData(25, 15)
    serviceRegistry = Mock()
    middlewareContext = new SportsMiddlewareContext(serviceRegistry, sportsCachedData)

    sportsCachedData.insertSportPageData(SocketIoTestHelper.getSportPageMapCache())
  }

  def "verify the  registerNewPageId"() {

    given:
    PageRawIndex pageRawIndex = PageRawIndex.fromPageId("222")

    when:
    middlewareContext.registerNewPageId(pageRawIndex)

    then:
    sportsCachedData.insertSportPageData(SocketIoTestHelper.getSportPageMapCache())
  }

  def "verify the  registerNewPageId with existing sportId"() {

    given:
    PageRawIndex pageRawIndex = PageRawIndex.fromPageId("16")

    when:
    middlewareContext.registerNewPageId(pageRawIndex)

    then:
    0 * sportsCachedData.insertSportPageData(SocketIoTestHelper.getSportPageMapCache())
  }

  def "verify the removePageIdFromCache"() {

    given:
    def sportId = "16"
    when:
    middlewareContext.removePageIdFromCache(sportId)
    then:
    sportsCachedData.removeSportIdFromSportPageMapCache(sportId)
  }

  def "verify the featuredService"() {

    given:
    serviceRegistry.getFeaturedService() >> new FeaturedServiceImpl()
    when:
    def service = middlewareContext.featuredService()
    then:
    service != null
  }


  def "verify the socketIOServer"() {

    given:
    serviceRegistry.getSocketIOServer() >> new SocketIOServer(new Configuration())
    when:
    def server = middlewareContext.socketIOServer()
    then:
    server != null
  }
}
