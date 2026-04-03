import asyncio
from asyncua import Client

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Assuming these are your Gmail credentials
gmail_user = "[EMAIL_ADDRESS]"
gmail_password = "[PASSWORD]"  # Use app password for security

url = "opc.tcp://10.10.10.136:4840"
#namespace = "PLC_PRAL"

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Find the namespace index
        #nsidx = await client.get_namespace_index(namespace)
        #print(f"Namespace Index for '{namespace}': {nsidx}")

        nsidx = 2 #me di cuenta que el valor es 2

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
                ["0:Objects", f"{nsidx}:M241-M251 data", f"{nsidx}:GVL.VOLTAJE_VII_AVG"]
        )
        
        while True:
            
            
            value = await var.read_value()
            print(f"Value of VOLTAJE AVG ({var}): {value}")

            # Check if the value is different from 0.0
            if value != 0.0:
                # Send email
                subject = "Alert: Non-zero Value Detected"
                body = f"The value of VOLTAJE AVG is {value}. This is an alert."

                msg = MIMEMultipart()
                msg['From'] = gmail_user
                msg['To'] = "[EMAIL_ADDRESS]"  # Change to your recipient's email address
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                try:
                    with smtplib.SMTP('smtp.gmail.com', 465) as server:
                        server.starttls()
                        server.login(gmail_user, gmail_password)
                        text = msg.as_string()
                        server.sendmail(gmail_user, msg['To'], text)
                        print("Email sent successfully!")
                except Exception as e:
                    print(f"Error sending email: {e}")
            
            # Cerrar la sesión explícitamente
            #await client.close_session()
            await asyncio.sleep(60)        

        
if __name__ == "__main__":
    asyncio.run(main())
