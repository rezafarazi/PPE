package com.cyberdyne.rezafta.PPERP.PPERP.Functions.TimeStep;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;

public class TimeStep
{

    public static long GetTimeStep(String timezone)
    {
        ZonedDateTime TimeZone=ZonedDateTime.now(ZoneId.of(timezone));
        LocalDateTime TimeZoneLocalDateTime = TimeZone.toLocalDateTime();
        Timestamp TimeStep=Timestamp.valueOf(TimeZoneLocalDateTime);

        return TimeStep.getTime();
    }


}
