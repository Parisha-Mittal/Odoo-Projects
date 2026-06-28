from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LaundryOrder(models.Model):
    _name = 'laundry.order'
    _description = 'Laundry Order'

    customer_name = fields.Char(
        string="Customer Name",
        required=True
    )

    mobile = fields.Char(
        string="Mobile Number",
        required=True
    )

    clothes = fields.Integer(
        string="Number of Clothes",
        required=True
    )

    bag_type = fields.Char(
        string="Required Bags",
        compute="_compute_bag",
        store=True
    )

    price = fields.Float(
        string="Total Price",
        compute="_compute_bag",
        store=True
    )

    payment_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('paid', 'Paid')
        ],
        string="Payment Status",
        default='pending'
    )

    order_status = fields.Selection(
        [
            ('new', 'New'),
            ('confirmed', 'Confirmed')
        ],
        string="Order Status",
        default='new'
    )

    confirmation_message = fields.Text(
        string="Confirmation Message"
    )

    # Prices
    SMALL_PRICE = 150
    MEDIUM_PRICE = 300
    LARGE_PRICE = 450

    @api.depends('clothes')
    def _compute_bag(self):
        """
        Automatically calculate:
        - Number of bags
        - Bag description
        - Total price
        """

        for rec in self:

            clothes = rec.clothes or 0

            large = clothes // 18
            remainder = clothes % 18

            medium = 0
            small = 0

            if remainder == 0:
                pass

            elif remainder <= 6:
                small = 1

            elif remainder <= 12:
                medium = 1

            else:
                large += 1

            bag_list = []

            if large:
                bag_list.append(f"{large} Large Bag")

            if medium:
                bag_list.append(f"{medium} Medium Bag")

            if small:
                bag_list.append(f"{small} Small Bag")

            if bag_list:
                rec.bag_type = ", ".join(bag_list)
            else:
                rec.bag_type = "No Bag"

            rec.price = (
                large * self.LARGE_PRICE +
                medium * self.MEDIUM_PRICE +
                small * self.SMALL_PRICE
            )

    @api.onchange('payment_status')
    def _onchange_payment(self):

        if self.payment_status == 'paid':
            self.order_status = 'confirmed'
            self.confirmation_message = (
                "Payment received. "
                "Your laundry order has been confirmed."
            )

        else:
            self.order_status = 'new'
            self.confirmation_message = ""

    @api.constrains('mobile')
    def _check_mobile(self):

        for rec in self:

            if not rec.mobile:
                continue

            if not rec.mobile.isdigit():
                raise ValidationError(
                    "Mobile number should contain only digits."
                )

            if len(rec.mobile) != 10:
                raise ValidationError(
                    "Mobile number must contain exactly 10 digits."
                )