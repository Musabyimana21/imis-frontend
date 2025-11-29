FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=development

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/sh\n\
echo "Starting IMIS Frontend..."\n\
echo "Waiting for backend..."\n\
while ! nc -z imis-backend 8000; do\n\
  echo "Backend not ready, waiting..."\n\
  sleep 2\n\
done\n\
echo "Backend ready! Starting IMIS Web..."\n\
npm run dev -- --host 0.0.0.0 --port 5173' > /app/start.sh

# Install netcat for health checks
RUN apk add --no-cache netcat-openbsd

RUN chmod +x /app/start.sh

EXPOSE 5173

CMD ["/app/start.sh"]
