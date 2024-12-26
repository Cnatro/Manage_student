import hashlib
import hmac
import urllib.parse


class VNPAY:
    def __init__(self):
        self.request_data = {}  # Dữ liệu yêu cầu gửi tới VNPAY
        self.response_data = {}  # Dữ liệu phản hồi từ VNPAY

    def get_payment_url(self, vnpay_payment_url, secret_key):
        """
        Tạo URL thanh toán để gửi đến VNPAY.
        """
        # Sắp xếp request_data theo thứ tự key
        input_data = sorted(self.request_data.items())

        # Tạo chuỗi query từ request_data
        query_string = '&'.join(f"{key}={urllib.parse.quote_plus(str(val))}" for key, val in input_data)

        # Tạo mã hash (chữ ký)
        secure_hash = self.__hmac_sha512(secret_key, query_string)

        # Tạo URL hoàn chỉnh
        return f"{vnpay_payment_url}?{query_string}&vnp_SecureHash={secure_hash}"

    def validate_response(self, secret_key):
        """
        Xác thực phản hồi từ VNPAY.
        """
        # Lấy mã hash từ response_data
        vnp_SecureHash = self.response_data.pop('vnp_SecureHash', None)

        # Sắp xếp response_data theo thứ tự key
        input_data = sorted(self.response_data.items())

        # Tạo chuỗi query từ response_data
        has_data = '&'.join(f"{key}={urllib.parse.quote_plus(str(val))}" for key, val in input_data)

        # Tạo mã hash để kiểm tra
        secure_hash = self.__hmac_sha512(secret_key, has_data)

        # Kiểm tra xem mã hash có khớp không
        return secure_hash == vnp_SecureHash

    @staticmethod
    def __hmac_sha512(key, data):
        """
        Tạo mã HMAC-SHA512.
        """
        byte_key = key.encode('utf-8')
        byte_data = data.encode('utf-8')
        return hmac.new(byte_key, byte_data, hashlib.sha512).hexdigest()
