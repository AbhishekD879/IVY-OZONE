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
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for Coupon complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="Coupon">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}event"/>
 *           &lt;/choice>
 *         &lt;/sequence>
 *       &lt;/choice>
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="classId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="couponSortCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="couponFlagCodes" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="displayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="isDisplayed" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="siteChannels" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="className" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="classDisplayOrder" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="classSortCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="classFlagCodes" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *       &lt;attribute name="categoryId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="categoryCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="categoryName" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="hasOpenEvent" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="hasNext24HourEvent" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="hasLiveNowEvent" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="hasLiveNowOrFutureEvent" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obBoolean" />
 *       &lt;attribute name="drilldownTagNames" type="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}obSetOfStrings" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "Coupon", propOrder = {
    "error",
    "event"
})
public class Coupon {

    protected Error error;
    protected List<Event> event;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String classId;
    @XmlAttribute
    protected String name;
    @XmlAttribute
    protected String couponSortCode;
    @XmlAttribute
    protected String couponFlagCodes;
    @XmlAttribute
    protected BigInteger displayOrder;
    @XmlAttribute
    protected String isDisplayed;
    @XmlAttribute
    protected String siteChannels;
    @XmlAttribute
    protected String className;
    @XmlAttribute
    protected BigInteger classDisplayOrder;
    @XmlAttribute
    protected String classSortCode;
    @XmlAttribute
    protected String classFlagCodes;
    @XmlAttribute
    protected String categoryId;
    @XmlAttribute
    protected String categoryCode;
    @XmlAttribute
    protected String categoryName;
    @XmlAttribute
    protected String hasOpenEvent;
    @XmlAttribute
    protected String hasNext24HourEvent;
    @XmlAttribute
    protected String hasLiveNowEvent;
    @XmlAttribute
    protected String hasLiveNowOrFutureEvent;
    @XmlAttribute
    protected String drilldownTagNames;

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
     * Gets the value of the event property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the event property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getEvent().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Event }
     * 
     * 
     */
    public List<Event> getEvent() {
        if (event == null) {
            event = new ArrayList<Event>();
        }
        return this.event;
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
     * Gets the value of the classId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClassId() {
        return classId;
    }

    /**
     * Sets the value of the classId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClassId(String value) {
        this.classId = value;
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
     * Gets the value of the couponSortCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCouponSortCode() {
        return couponSortCode;
    }

    /**
     * Sets the value of the couponSortCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCouponSortCode(String value) {
        this.couponSortCode = value;
    }

    /**
     * Gets the value of the couponFlagCodes property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCouponFlagCodes() {
        return couponFlagCodes;
    }

    /**
     * Sets the value of the couponFlagCodes property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCouponFlagCodes(String value) {
        this.couponFlagCodes = value;
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
     * Gets the value of the className property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClassName() {
        return className;
    }

    /**
     * Sets the value of the className property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClassName(String value) {
        this.className = value;
    }

    /**
     * Gets the value of the classDisplayOrder property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getClassDisplayOrder() {
        return classDisplayOrder;
    }

    /**
     * Sets the value of the classDisplayOrder property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setClassDisplayOrder(BigInteger value) {
        this.classDisplayOrder = value;
    }

    /**
     * Gets the value of the classSortCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClassSortCode() {
        return classSortCode;
    }

    /**
     * Sets the value of the classSortCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClassSortCode(String value) {
        this.classSortCode = value;
    }

    /**
     * Gets the value of the classFlagCodes property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClassFlagCodes() {
        return classFlagCodes;
    }

    /**
     * Sets the value of the classFlagCodes property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClassFlagCodes(String value) {
        this.classFlagCodes = value;
    }

    /**
     * Gets the value of the categoryId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCategoryId() {
        return categoryId;
    }

    /**
     * Sets the value of the categoryId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCategoryId(String value) {
        this.categoryId = value;
    }

    /**
     * Gets the value of the categoryCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCategoryCode() {
        return categoryCode;
    }

    /**
     * Sets the value of the categoryCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCategoryCode(String value) {
        this.categoryCode = value;
    }

    /**
     * Gets the value of the categoryName property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCategoryName() {
        return categoryName;
    }

    /**
     * Sets the value of the categoryName property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCategoryName(String value) {
        this.categoryName = value;
    }

    /**
     * Gets the value of the hasOpenEvent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasOpenEvent() {
        return hasOpenEvent;
    }

    /**
     * Sets the value of the hasOpenEvent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasOpenEvent(String value) {
        this.hasOpenEvent = value;
    }

    /**
     * Gets the value of the hasNext24HourEvent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasNext24HourEvent() {
        return hasNext24HourEvent;
    }

    /**
     * Sets the value of the hasNext24HourEvent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasNext24HourEvent(String value) {
        this.hasNext24HourEvent = value;
    }

    /**
     * Gets the value of the hasLiveNowEvent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasLiveNowEvent() {
        return hasLiveNowEvent;
    }

    /**
     * Sets the value of the hasLiveNowEvent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasLiveNowEvent(String value) {
        this.hasLiveNowEvent = value;
    }

    /**
     * Gets the value of the hasLiveNowOrFutureEvent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getHasLiveNowOrFutureEvent() {
        return hasLiveNowOrFutureEvent;
    }

    /**
     * Sets the value of the hasLiveNowOrFutureEvent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setHasLiveNowOrFutureEvent(String value) {
        this.hasLiveNowOrFutureEvent = value;
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

}
