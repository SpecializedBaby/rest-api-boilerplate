from fastcrud import FastCRUD

from ..models.fund import Fund
from ..schemas.fund import FundCreate

CRUDFund = FastCRUD[Fund, FundCreate]
crud_funds = CRUDFund(Fund)
