from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from app.models import UserSchema, FileMetadataSchema
from app.database import users_collection, files_collection
from app.crypto_engine import encrypt_file_hybrid
from app.storage import upload_file_async
from Crypto.PublicKey import RSA
import uuid

app = FastAPI(title="Cryptography as a Service")

@app.post("/register")
async def register_user(user: UserSchema):
    # Generate RSA Keys for the user
    key = RSA.generate(2048)
    public_key = key.publickey().export_key().decode('utf-8')
    private_key = key.export_key().decode('utf-8') # In real app, user downloads this immediately
    
    user_dict = user.dict()
    user_dict['rsa_public_key'] = public_key
    
    await users_collection.insert_one(user_dict)
    return {"message": "Registered", "private_key": private_key}

@app.post("/upload")
async def upload_file(username: str, file: UploadFile = File(...)):
    # 1. Fetch User's Public Key
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    file_content = await file.read()
    
    # 2. Hybrid Encryption (CPU Intensive)
    encrypted_data = encrypt_file_hybrid(file_content, user['rsa_public_key'])
    
    # 3. Async GCS Upload (I/O Bound - Offloaded to thread)
    gcs_path = f"{username}/{uuid.uuid4()}.bin"
    storage_url = await upload_file_async(encrypted_data['ciphertext'], gcs_path)
    
    # 4. Store Metadata (Async Non-blocking)
    metadata = {
        "owner": username,
        "gcs_path": gcs_path,
        "encrypted_aes_key": encrypted_data['encrypted_aes_key'], # Stored as bytes
        "nonce": encrypted_data['nonce'],
        "tag": encrypted_data['tag']
    }
    await files_collection.insert_one(metadata)
    
    return {"status": "Securely Uploaded", "path": storage_url}