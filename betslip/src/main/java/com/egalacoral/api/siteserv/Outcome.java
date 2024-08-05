//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for Outcome complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Outcome">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}price"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}historicPrice"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}statistic"/>
 *           &lt;/choice>
 *         &lt;/sequence>
 *       &lt;/choice>
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="marketId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="outcomeMeaningMajorCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="outcomeMeaningMinorCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="outcomeMeaningScores" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obListOfStrings" />
 *       &lt;attribute name="runnerNumber" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="isResulted" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="displayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="outcomeStatusCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isActive" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="liveServChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="liveServChildrenChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="liveServLastMsgId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="drilldownTagNames" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="isAvailable" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isFinished" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="hasRestrictedSet" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="isEnhancedOdds" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="cashoutAvail" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Outcome", propOrder = {
    "error",
    "priceOrHistoricPriceOrStatistic"
})
public class Outcome {

    protected Error error;
    @XmlElements({
        @XmlElement(name = "statistic", type = Statistic.class),
        @XmlElement(name = "price", type = Price.class),
        @XmlElement(name = "historicPrice", type = HistoricPrice.class)
    })
    protected List<Object> priceOrHistoricPriceOrStatistic;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String marketId;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected String outcomeMeaningMajorCode;
    @XmlAttribute
    protected String outcomeMeaningMinorCode;
    @XmlAttribute
    protected String outcomeMeaningScores;
    @XmlAttribute
    protected BigInteger runnerNumber;
    @XmlAttribute
    protected String isResulted;
    @XmlAttribute
    protected BigInteger displayOrder;
    @XmlAttribute
    protected String outcomeStatusCode;
    @XmlAttribute
    protected String isActive;
    @XmlAttribute
    protected String isDisplayed;
    @XmlAttribute
    protected String siteChannels;
    @XmlAttribute
    protected String liveServChannels;
    @XmlAttribute
    protected String liveServChildrenChannels;
    @XmlAttribute
    protected String liveServLastMsgId;
    @XmlAttribute
    protected String drilldownTagNames;
    @XmlAttribute
    protected String isAvailable;
    @XmlAttribute
    protected String isFinished;
    @XmlAttribute
    protected String hasRestrictedSet;
    @XmlAttribute
    protected String isEnhancedOdds;
    @XmlAttribute
    protected String cashoutAvail;

    /**
     * Gets the value of the error property.
     * 
     * @return
     *     possible object is
     *     {@link Error }
     *     
     */
    public Error getError() {
        return error;
    }

    /**
     * Sets the value of the error property.
     * 
     * @param value
     *     allowed object is
     *     {@link Error }
     *     
     */
    public void setError(Error value) {
        this.error = value;
    }

    /**
     * Gets the value of the priceOrHistoricPriceOrStatistic property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the priceOrHistoricPriceOrStatistic property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getPriceOrHistoricPriceOrStatistic().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Statistic }
     * {@link Price }
     * {@link HistoricPrice }
     * 
     * 
     */
    public List<Object> getPriceOrHistoricPriceOrStatistic() {
        if (priceOrHistoricPriceOrStatistic == null) {
            priceOrHistoricPriceOrStatistic = new ArrayList<Object>();
        }
        return this.priceOrHistoricPriceOrStatistic;
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    /**
     * Gets the value of the marketId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getMarketId() {
        return marketId;
    }

    /**
     * Sets the value of the marketId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setMarketId(String value) {
        this.marketId = value;
    }

    /**
     * Gets the value of the name property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the value of the name property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setName(String value) {
        this.name = value;
    }

    /**
     * Gets the value of the outcomeMeaningMajorCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeMeaningMajorCode() {
        return outcomeMeaningMajorCode;
    }

    /**
     * Sets the value of the outcomeMeaningMajorCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeMeaningMajorCode(String value) {
        this.outcomeMeaningMajorCode = value;
    }

    /**
     * Gets the value of the outcomeMeaningMinorCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeMeaningMinorCode() {
        return outcomeMeaningMinorCode;
    }

    /**
     * Sets the value of the outcomeMeaningMinorCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeMeaningMinorCode(String value) {
        this.outcomeMeaningMinorCode = value;
    }

    /**
     * Gets the value of the outcomeMeaningScores property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeMeaningScores() {
        return outcomeMeaningScores;
    }

    /**
     * Sets the value of the outcomeMeaningScores property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeMeaningScores(String value) {
        this.outcomeMeaningScores = value;
    }

    /**
     * Gets the value of the runnerNumber property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getRunnerNumber() {
        return runnerNumber;
    }

    /**
     * Sets the value of the runnerNumber property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setRunnerNumber(BigInteger value) {
        this.runnerNumber = value;
    }

    /**
     * Gets the value of the isResulted property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsResulted() {
        return isResulted;
    }

    /**
     * Sets the value of the isResulted property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsResulted(String value) {
        this.isResulted = value;
    }

    /**
     * Gets the value of the displayOrder property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getDisplayOrder() {
        return displayOrder;
    }

    /**
     * Sets the value of the displayOrder property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setDisplayOrder(BigInteger value) {
        this.displayOrder = value;
    }

    /**
     * Gets the value of the outcomeStatusCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getOutcomeStatusCode() {
        return outcomeStatusCode;
    }

    /**
     * Sets the value of the outcomeStatusCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setOutcomeStatusCode(String value) {
        this.outcomeStatusCode = value;
    }

    /**
     * Gets the value of the isActive property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsActive() {
        return isActive;
    }

    /**
     * Sets the value of the isActive property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsActive(String value) {
        this.isActive = value;
    }

    /**
     * Gets the value of the isDisplayed property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsDisplayed() {
        return isDisplayed;
    }

    /**
     * Sets the value of the isDisplayed property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsDisplayed(String value) {
        this.isDisplayed = value;
    }

    /**
     * Gets the value of the siteChannels property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSiteChannels() {
        return siteChannels;
    }

    /**
     * Sets the value of the siteChannels property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSiteChannels(String value) {
        this.siteChannels = value;
    }

    /**
     * Gets the value of the liveServChannels property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLiveServChannels() {
        return liveServChannels;
    }

    /**
     * Sets the value of the liveServChannels property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLiveServChannels(String value) {
        this.liveServChannels = value;
    }

    /**
     * Gets the value of the liveServChildrenChannels property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLiveServChildrenChannels() {
        return liveServChildrenChannels;
    }

    /**
     * Sets the value of the liveServChildrenChannels property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLiveServChildrenChannels(String value) {
        this.liveServChildrenChannels = value;
    }

    /**
     * Gets the value of the liveServLastMsgId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLiveServLastMsgId() {
        return liveServLastMsgId;
    }

    /**
     * Sets the value of the liveServLastMsgId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLiveServLastMsgId(String value) {
        this.liveServLastMsgId = value;
    }

    /**
     * Gets the value of the drilldownTagNames property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDrilldownTagNames() {
        return drilldownTagNames;
    }

    /**
     * Sets the value of the drilldownTagNames property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDrilldownTagNames(String value) {
        this.drilldownTagNames = value;
    }

    /**
     * Gets the value of the isAvailable property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsAvailable() {
        return isAvailable;
    }

    /**
     * Sets the value of the isAvailable property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsAvailable(String value) {
        this.isAvailable = value;
    }

    /**
     * Gets the value of the isFinished property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsFinished() {
        return isFinished;
    }

    /**
     * Sets the value of the isFinished property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsFinished(String value) {
        this.isFinished = value;
    }

    /**
     * Gets the value of the hasRestrictedSet property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasRestrictedSet() {
        return hasRestrictedSet;
    }

    /**
     * Sets the value of the hasRestrictedSet property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasRestrictedSet(String value) {
        this.hasRestrictedSet = value;
    }

    /**
     * Gets the value of the isEnhancedOdds property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIsEnhancedOdds() {
        return isEnhancedOdds;
    }

    /**
     * Sets the value of the isEnhancedOdds property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIsEnhancedOdds(String value) {
        this.isEnhancedOdds = value;
    }

    /**
     * Gets the value of the cashoutAvail property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCashoutAvail() {
        return cashoutAvail;
    }

    /**
     * Sets the value of the cashoutAvail property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCashoutAvail(String value) {
        this.cashoutAvail = value;
    }

}
