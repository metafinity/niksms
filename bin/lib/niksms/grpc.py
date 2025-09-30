import grpc
from . import Service_pb2, Service_pb2_grpc
from typing import List, Optional

class NiksmsGrpcClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Use fixed gRPC URL
        grpc_url = "grpc.niksms.com:443"
        # Use secure channel for public gRPC endpoint
        self.channel = grpc.secure_channel(grpc_url, grpc.ssl_channel_credentials())

        self.stub = Service_pb2_grpc.GrpcWebServiceStub(self.channel)

    def send_single(self, sender_number: str, phone: str, message: str, message_id: Optional[str]=None, send_date: Optional[str]=None, send_type: Optional[int]=None, api_type: Optional[int]=1):
        req = Service_pb2.GrpcWebServiceSendSmsSingleRequest(
            ApiKey=self.api_key,
            SenderNumber=sender_number,
            Phone=phone,
            Message=message,
            ServiceType="SDK_Python",
            ApiType=api_type
        )
        if message_id: req.MessageId = message_id
        if send_type: req.SendType = send_type
        # send_date: باید به google.protobuf.Timestamp تبدیل شود (در نسخه بعدی اضافه می‌شود)
        grpc_req = Service_pb2.GrpcWebService_SendSingleReq(Request=req)
        return self.stub.SendSingle(grpc_req)

    def send_group(self, sender_number: str, message: str, recipients: List[dict], send_date: Optional[str]=None, send_type: Optional[int]=None, api_type: Optional[int]=1):
        recs = [Service_pb2.GrpcWebServiceGroupSmsRecipient(Phone=r['Phone'], MessageId=r['MessageId']) for r in recipients]
        req = Service_pb2.GrpcWebServiceSendSmsGroupRequest(
            ApiKey=self.api_key,
            SenderNumber=sender_number,
            Message=message,
            Recipients=recs,
            ServiceType="SDK_Python",
            ApiType=api_type
        )
        if send_type: req.SendType = send_type
        grpc_req = Service_pb2.GrpcWebService_SendGroupReq(Request=req)
        return self.stub.SendGroup(grpc_req)

    def send_ptp(self, sender_number: str, recipients: List[dict], send_date: Optional[str]=None, send_type: Optional[int]=None, api_type: Optional[int]=1):
        recs = [Service_pb2.GrpcWebServicePtpSmsRecipient(Message=r['Message'], Phone=r['Phone'], MessageId=r['MessageId']) for r in recipients]
        req = Service_pb2.GrpcWebServiceSendSmsPtpRequest(
            ApiKey=self.api_key,
            SenderNumber=sender_number,
            Recipients=recs,
            ServiceType="SDK_Python",
            ApiType=api_type
        )
        if send_type: req.SendType = send_type
        grpc_req = Service_pb2.GrpcWebService_SendPtpReq(Request=req)
        return self.stub.SendPtp(grpc_req)

    def send_otp(self, sender_number: str, phone: str, message: str, message_id: Optional[str]=None, send_date: Optional[str]=None, send_type: Optional[int]=None, api_type: Optional[int]=1):
        req = Service_pb2.GrpcWebServiceSendSmsOtpRequest(
            ApiKey=self.api_key,
            SenderNumber=sender_number,
            Phone=phone,
            Message=message,
            ServiceType="SDK_Python",
            ApiType=api_type
        )
        if message_id: req.MessageId = message_id
        if send_type: req.SendType = send_type
        grpc_req = Service_pb2.GrpcWebService_SendOtpReq(Request=req)
        return self.stub.SendOtp(grpc_req)

    def get_credit(self, api_type: Optional[int]=1):
        req = Service_pb2.GrpcWebServiceGetCreditRequest(ApiKey=self.api_key, ServiceType="SDK_Python", ApiType=api_type)
        grpc_req = Service_pb2.GrpcWebService_GetCreditReq(Request=req)
        return self.stub.GetCredit(grpc_req)

    def get_panel_expire_date(self, api_type: Optional[int]=1):
        req = Service_pb2.GrpcWebServiceGetPanelExpireDateRequest(ApiKey=self.api_key, ServiceType="SDK_Python", ApiType=api_type)
        grpc_req = Service_pb2.GrpcWebService_GetPanelExpireDateReq(Request=req)
        return self.stub.GetPanelExpireDate(grpc_req)

    def get_sms_status(self, message_ids: List[str], api_type: Optional[int]=1):
        req = Service_pb2.GrpcWebServiceGetSmsStatusRequest(ApiKey=self.api_key, MessageIds=message_ids, ServiceType="SDK_Python", ApiType=api_type)
        grpc_req = Service_pb2.GrpcWebService_SmsStatusReq(Request=req)
        return self.stub.SmsStatus(grpc_req)
