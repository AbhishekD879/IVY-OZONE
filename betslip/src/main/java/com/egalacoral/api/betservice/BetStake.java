//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;
import javax.xml.namespace.QName;


/**
 * <p>Java class for betStake complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="betStake">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="currencyRef" type="{http://schema.openbet.com/core}entityRef"/>
 *         &lt;element name="funding" maxOccurs="unbounded" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element name="transactionRef" type="{http://schema.openbet.com/core}entityRef"/>
 *                 &lt;/sequence>
 *                 &lt;attribute name="amount" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/sequence>
 *       &lt;attribute name="amount" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="requested" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="funded" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="freebet" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="minAllowed" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="maxAllowed" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="stakeFactor" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="stakePerLine" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "betStake", propOrder = {
    "currencyRef",
    "funding"
})
public class BetStake
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    @XmlElement(required = true)
    protected EntityRef currencyRef;
    protected List<Funding> funding;
    @XmlAttribute
    protected BigDecimal amount;
    @XmlAttribute
    protected BigDecimal requested;
    @XmlAttribute
    protected BigDecimal funded;
    @XmlAttribute
    protected BigDecimal freebet;
    @XmlAttribute
    protected BigDecimal minAllowed;
    @XmlAttribute
    protected BigDecimal maxAllowed;
    @XmlAttribute
    protected BigDecimal stakeFactor;
    @XmlAttribute
    protected BigDecimal stakePerLine;
    @XmlAnyAttribute
    private Map<QName, String> otherAttributes = new HashMap<QName, String>();

    /**
     * Gets the value of the currencyRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getCurrencyRef() {
        return currencyRef;
    }

    /**
     * Sets the value of the currencyRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setCurrencyRef(EntityRef value) {
        this.currencyRef = value;
    }

    public boolean isSetCurrencyRef() {
        return (this.currencyRef!= null);
    }

    /**
     * Gets the value of the funding property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the funding property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getFunding().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Funding }
     * 
     * 
     */
    public List<Funding> getFunding() {
        if (funding == null) {
            funding = new ArrayList<Funding>();
        }
        return this.funding;
    }

    public boolean isSetFunding() {
        return ((this.funding!= null)&&(!this.funding.isEmpty()));
    }

    public void unsetFunding() {
        this.funding = null;
    }

    /**
     * Gets the value of the amount property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getAmount() {
        return amount;
    }

    /**
     * Sets the value of the amount property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setAmount(BigDecimal value) {
        this.amount = value;
    }

    public boolean isSetAmount() {
        return (this.amount!= null);
    }

    /**
     * Gets the value of the requested property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getRequested() {
        return requested;
    }

    /**
     * Sets the value of the requested property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setRequested(BigDecimal value) {
        this.requested = value;
    }

    public boolean isSetRequested() {
        return (this.requested!= null);
    }

    /**
     * Gets the value of the funded property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getFunded() {
        return funded;
    }

    /**
     * Sets the value of the funded property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setFunded(BigDecimal value) {
        this.funded = value;
    }

    public boolean isSetFunded() {
        return (this.funded!= null);
    }

    /**
     * Gets the value of the freebet property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getFreebet() {
        return freebet;
    }

    /**
     * Sets the value of the freebet property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setFreebet(BigDecimal value) {
        this.freebet = value;
    }

    public boolean isSetFreebet() {
        return (this.freebet!= null);
    }

    /**
     * Gets the value of the minAllowed property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getMinAllowed() {
        return minAllowed;
    }

    /**
     * Sets the value of the minAllowed property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setMinAllowed(BigDecimal value) {
        this.minAllowed = value;
    }

    public boolean isSetMinAllowed() {
        return (this.minAllowed!= null);
    }

    /**
     * Gets the value of the maxAllowed property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getMaxAllowed() {
        return maxAllowed;
    }

    /**
     * Sets the value of the maxAllowed property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setMaxAllowed(BigDecimal value) {
        this.maxAllowed = value;
    }

    public boolean isSetMaxAllowed() {
        return (this.maxAllowed!= null);
    }

    /**
     * Gets the value of the stakeFactor property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getStakeFactor() {
        return stakeFactor;
    }

    /**
     * Sets the value of the stakeFactor property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setStakeFactor(BigDecimal value) {
        this.stakeFactor = value;
    }

    public boolean isSetStakeFactor() {
        return (this.stakeFactor!= null);
    }

    /**
     * Gets the value of the stakePerLine property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getStakePerLine() {
        return stakePerLine;
    }

    /**
     * Sets the value of the stakePerLine property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setStakePerLine(BigDecimal value) {
        this.stakePerLine = value;
    }

    public boolean isSetStakePerLine() {
        return (this.stakePerLine!= null);
    }

    /**
     * Gets a map that contains attributes that aren't bound to any typed property on this class.
     * 
     * <p>
     * the map is keyed by the name of the attribute and 
     * the value is the string value of the attribute.
     * 
     * the map returned by this method is live, and you can add new attribute
     * by updating the map directly. Because of this design, there's no setter.
     * 
     * 
     * @return
     *     always non-null
     */
    public Map<QName, String> getOtherAttributes() {
        return otherAttributes;
    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;sequence>
     *         &lt;element name="transactionRef" type="{http://schema.openbet.com/core}entityRef"/>
     *       &lt;/sequence>
     *       &lt;attribute name="amount" type="{http://www.w3.org/2001/XMLSchema}decimal" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "transactionRef"
    })
    public static class Funding
        implements Serializable
    {

        private final static long serialVersionUID = 1L;
        @XmlElement(required = true)
        protected EntityRef transactionRef;
        @XmlAttribute
        protected BigDecimal amount;
        @XmlAnyAttribute
        private Map<QName, String> otherAttributes = new HashMap<QName, String>();

        /**
         * Gets the value of the transactionRef property.
         * 
         * @return
         *     possible object is
         *     {@link EntityRef }
         *     
         */
        public EntityRef getTransactionRef() {
            return transactionRef;
        }

        /**
         * Sets the value of the transactionRef property.
         * 
         * @param value
         *     allowed object is
         *     {@link EntityRef }
         *     
         */
        public void setTransactionRef(EntityRef value) {
            this.transactionRef = value;
        }

        public boolean isSetTransactionRef() {
            return (this.transactionRef!= null);
        }

        /**
         * Gets the value of the amount property.
         * 
         * @return
         *     possible object is
         *     {@link BigDecimal }
         *     
         */
        public BigDecimal getAmount() {
            return amount;
        }

        /**
         * Sets the value of the amount property.
         * 
         * @param value
         *     allowed object is
         *     {@link BigDecimal }
         *     
         */
        public void setAmount(BigDecimal value) {
            this.amount = value;
        }

        public boolean isSetAmount() {
            return (this.amount!= null);
        }

        /**
         * Gets a map that contains attributes that aren't bound to any typed property on this class.
         * 
         * <p>
         * the map is keyed by the name of the attribute and 
         * the value is the string value of the attribute.
         * 
         * the map returned by this method is live, and you can add new attribute
         * by updating the map directly. Because of this design, there's no setter.
         * 
         * 
         * @return
         *     always non-null
         */
        public Map<QName, String> getOtherAttributes() {
            return otherAttributes;
        }

    }

}
