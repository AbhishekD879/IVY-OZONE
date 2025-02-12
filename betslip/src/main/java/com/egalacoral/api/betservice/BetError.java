//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for betError complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="betError">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="errorDesc" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="legPartRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="legRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="betRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="outcomeRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="overrideRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="price" type="{http://schema.products.sportsbook.openbet.com/betcommon}price" maxOccurs="2" minOccurs="0"/>
 *         &lt;element name="cashoutValue" type="{http://schema.products.sportsbook.openbet.com/bet}cashoutValue" minOccurs="0"/>
 *         &lt;element name="cashoutDelay" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="cashoutBetDelayId" type="{http://www.w3.org/2001/XMLSchema}string" minOccurs="0"/>
 *         &lt;element name="range" type="{http://schema.products.sportsbook.openbet.com/betcommon}range" minOccurs="0"/>
 *         &lt;element name="updateExternalRef" type="{http://schema.products.sportsbook.openbet.com/bet}updateExternalRef" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="code" type="{http://schema.products.sportsbook.openbet.com/bet}topErrorCode" />
 *       &lt;attribute name="subErrorCode" type="{http://schema.products.sportsbook.openbet.com/bet}subErrorCode" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "betError", propOrder = {
    "errorDesc",
    "legPartRef",
    "legRef",
    "betRef",
    "outcomeRef",
    "overrideRef",
    "price",
    "cashoutValue",
    "cashoutDelay",
    "cashoutBetDelayId",
    "range",
    "updateExternalRef"
})
public class BetError
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    protected String errorDesc;
    protected List<EntityRef> legPartRef;
    protected List<EntityRef> legRef;
    protected List<EntityRef> betRef;
    protected List<EntityRef> outcomeRef;
    protected List<EntityRef> overrideRef;
    protected List<Price> price;
    protected CashoutValue cashoutValue;
    protected String cashoutDelay;
    protected String cashoutBetDelayId;
    protected Range range;
    protected List<UpdateExternalRef> updateExternalRef;
    @XmlAttribute
    protected TopErrorCode code;
    @XmlAttribute
    protected SubErrorCode subErrorCode;

    /**
     * Gets the value of the errorDesc property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getErrorDesc() {
        return errorDesc;
    }

    /**
     * Sets the value of the errorDesc property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setErrorDesc(String value) {
        this.errorDesc = value;
    }

    public boolean isSetErrorDesc() {
        return (this.errorDesc!= null);
    }

    /**
     * Gets the value of the legPartRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the legPartRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLegPartRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getLegPartRef() {
        if (legPartRef == null) {
            legPartRef = new ArrayList<EntityRef>();
        }
        return this.legPartRef;
    }

    public boolean isSetLegPartRef() {
        return ((this.legPartRef!= null)&&(!this.legPartRef.isEmpty()));
    }

    public void unsetLegPartRef() {
        this.legPartRef = null;
    }

    /**
     * Gets the value of the legRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the legRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLegRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getLegRef() {
        if (legRef == null) {
            legRef = new ArrayList<EntityRef>();
        }
        return this.legRef;
    }

    public boolean isSetLegRef() {
        return ((this.legRef!= null)&&(!this.legRef.isEmpty()));
    }

    public void unsetLegRef() {
        this.legRef = null;
    }

    /**
     * Gets the value of the betRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the betRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getBetRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getBetRef() {
        if (betRef == null) {
            betRef = new ArrayList<EntityRef>();
        }
        return this.betRef;
    }

    public boolean isSetBetRef() {
        return ((this.betRef!= null)&&(!this.betRef.isEmpty()));
    }

    public void unsetBetRef() {
        this.betRef = null;
    }

    /**
     * Gets the value of the outcomeRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the outcomeRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOutcomeRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getOutcomeRef() {
        if (outcomeRef == null) {
            outcomeRef = new ArrayList<EntityRef>();
        }
        return this.outcomeRef;
    }

    public boolean isSetOutcomeRef() {
        return ((this.outcomeRef!= null)&&(!this.outcomeRef.isEmpty()));
    }

    public void unsetOutcomeRef() {
        this.outcomeRef = null;
    }

    /**
     * Gets the value of the overrideRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the overrideRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOverrideRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getOverrideRef() {
        if (overrideRef == null) {
            overrideRef = new ArrayList<EntityRef>();
        }
        return this.overrideRef;
    }

    public boolean isSetOverrideRef() {
        return ((this.overrideRef!= null)&&(!this.overrideRef.isEmpty()));
    }

    public void unsetOverrideRef() {
        this.overrideRef = null;
    }

    /**
     * Gets the value of the price property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the price property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getPrice().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Price }
     * 
     * 
     */
    public List<Price> getPrice() {
        if (price == null) {
            price = new ArrayList<Price>();
        }
        return this.price;
    }

    public boolean isSetPrice() {
        return ((this.price!= null)&&(!this.price.isEmpty()));
    }

    public void unsetPrice() {
        this.price = null;
    }

    /**
     * Gets the value of the cashoutValue property.
     * 
     * @return
     *     possible object is
     *     {@link CashoutValue }
     *     
     */
    public CashoutValue getCashoutValue() {
        return cashoutValue;
    }

    /**
     * Sets the value of the cashoutValue property.
     * 
     * @param value
     *     allowed object is
     *     {@link CashoutValue }
     *     
     */
    public void setCashoutValue(CashoutValue value) {
        this.cashoutValue = value;
    }

    public boolean isSetCashoutValue() {
        return (this.cashoutValue!= null);
    }

    /**
     * Gets the value of the cashoutDelay property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCashoutDelay() {
        return cashoutDelay;
    }

    /**
     * Sets the value of the cashoutDelay property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCashoutDelay(String value) {
        this.cashoutDelay = value;
    }

    public boolean isSetCashoutDelay() {
        return (this.cashoutDelay!= null);
    }

    /**
     * Gets the value of the cashoutBetDelayId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getCashoutBetDelayId() {
        return cashoutBetDelayId;
    }

    /**
     * Sets the value of the cashoutBetDelayId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setCashoutBetDelayId(String value) {
        this.cashoutBetDelayId = value;
    }

    public boolean isSetCashoutBetDelayId() {
        return (this.cashoutBetDelayId!= null);
    }

    /**
     * Gets the value of the range property.
     * 
     * @return
     *     possible object is
     *     {@link Range }
     *     
     */
    public Range getRange() {
        return range;
    }

    /**
     * Sets the value of the range property.
     * 
     * @param value
     *     allowed object is
     *     {@link Range }
     *     
     */
    public void setRange(Range value) {
        this.range = value;
    }

    public boolean isSetRange() {
        return (this.range!= null);
    }

    /**
     * Gets the value of the updateExternalRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the updateExternalRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getUpdateExternalRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link UpdateExternalRef }
     * 
     * 
     */
    public List<UpdateExternalRef> getUpdateExternalRef() {
        if (updateExternalRef == null) {
            updateExternalRef = new ArrayList<UpdateExternalRef>();
        }
        return this.updateExternalRef;
    }

    public boolean isSetUpdateExternalRef() {
        return ((this.updateExternalRef!= null)&&(!this.updateExternalRef.isEmpty()));
    }

    public void unsetUpdateExternalRef() {
        this.updateExternalRef = null;
    }

    /**
     * Gets the value of the code property.
     * 
     * @return
     *     possible object is
     *     {@link TopErrorCode }
     *     
     */
    public TopErrorCode getCode() {
        return code;
    }

    /**
     * Sets the value of the code property.
     * 
     * @param value
     *     allowed object is
     *     {@link TopErrorCode }
     *     
     */
    public void setCode(TopErrorCode value) {
        this.code = value;
    }

    public boolean isSetCode() {
        return (this.code!= null);
    }

    /**
     * Gets the value of the subErrorCode property.
     * 
     * @return
     *     possible object is
     *     {@link SubErrorCode }
     *     
     */
    public SubErrorCode getSubErrorCode() {
        return subErrorCode;
    }

    /**
     * Sets the value of the subErrorCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link SubErrorCode }
     *     
     */
    public void setSubErrorCode(SubErrorCode value) {
        this.subErrorCode = value;
    }

    public boolean isSetSubErrorCode() {
        return (this.subErrorCode!= null);
    }

}
