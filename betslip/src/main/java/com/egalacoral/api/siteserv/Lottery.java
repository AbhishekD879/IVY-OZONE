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
 * <p>Java class for Lottery complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Lottery">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}lotteryPrice"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}draw"/>
 *           &lt;/choice>
 *         &lt;/sequence>
 *       &lt;/choice>
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="sort" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="description" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="minPicks" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="maxPicks" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="maxLines" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="minNumber" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="maxNumber" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="hasOpenDraw" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Lottery", propOrder = {
    "error",
    "lotteryPriceOrDraw"
})
public class Lottery {

    protected Error error;
    @XmlElements({
        @XmlElement(name = "lotteryPrice", type = LotteryPrice.class),
        @XmlElement(name = "draw", type = Draw.class)
    })
    protected List<Object> lotteryPriceOrDraw;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String sort;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected String description;
    @XmlAttribute
    protected String siteChannels;
    @XmlAttribute
    protected BigInteger minPicks;
    @XmlAttribute
    protected BigInteger maxPicks;
    @XmlAttribute
    protected BigInteger maxLines;
    @XmlAttribute
    protected BigInteger minNumber;
    @XmlAttribute
    protected BigInteger maxNumber;
    @XmlAttribute
    protected String hasOpenDraw;

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
     * Gets the value of the lotteryPriceOrDraw property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the lotteryPriceOrDraw property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLotteryPriceOrDraw().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link LotteryPrice }
     * {@link Draw }
     * 
     * 
     */
    public List<Object> getLotteryPriceOrDraw() {
        if (lotteryPriceOrDraw == null) {
            lotteryPriceOrDraw = new ArrayList<Object>();
        }
        return this.lotteryPriceOrDraw;
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
     * Gets the value of the sort property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getSort() {
        return sort;
    }

    /**
     * Sets the value of the sort property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setSort(String value) {
        this.sort = value;
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
     * Gets the value of the description property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the value of the description property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDescription(String value) {
        this.description = value;
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
     * Gets the value of the minPicks property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMinPicks() {
        return minPicks;
    }

    /**
     * Sets the value of the minPicks property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMinPicks(BigInteger value) {
        this.minPicks = value;
    }

    /**
     * Gets the value of the maxPicks property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMaxPicks() {
        return maxPicks;
    }

    /**
     * Sets the value of the maxPicks property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMaxPicks(BigInteger value) {
        this.maxPicks = value;
    }

    /**
     * Gets the value of the maxLines property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMaxLines() {
        return maxLines;
    }

    /**
     * Sets the value of the maxLines property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMaxLines(BigInteger value) {
        this.maxLines = value;
    }

    /**
     * Gets the value of the minNumber property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMinNumber() {
        return minNumber;
    }

    /**
     * Sets the value of the minNumber property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMinNumber(BigInteger value) {
        this.minNumber = value;
    }

    /**
     * Gets the value of the maxNumber property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getMaxNumber() {
        return maxNumber;
    }

    /**
     * Sets the value of the maxNumber property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setMaxNumber(BigInteger value) {
        this.maxNumber = value;
    }

    /**
     * Gets the value of the hasOpenDraw property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasOpenDraw() {
        return hasOpenDraw;
    }

    /**
     * Sets the value of the hasOpenDraw property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasOpenDraw(String value) {
        this.hasOpenDraw = value;
    }

}
