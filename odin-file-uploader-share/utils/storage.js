const cloudinary = require("../config/cloudinary");

function uploadBuffer(buffer, userId) {
  return new Promise((resolve, reject) => {
    const stream = cloudinary.uploader.upload_stream(
      {
        folder: `file-uploader/user-${userId}`,
        resource_type: "auto",
        unique_filename: true,
        overwrite: false,
      },
      (error, result) => (error ? reject(error) : resolve(result)),
    );

    stream.end(buffer);
  });
}

function deleteStored({ publicId, resourceType }) {
  return cloudinary.uploader.destroy(publicId, { resource_type: resourceType });
}

module.exports = { uploadBuffer, deleteStored };
